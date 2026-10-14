#!/usr/bin/env python3
"""Minimal CDP client over Chromium's --remote-debugging-pipe transport.

Yuque's Electron main process force-quits when it sees --inspect /
--remote-debugging-port in process.argv, so we use the pipe transport and
talk CDP over fd 3 (read) / fd 4 (write).
"""
import json
import os
import subprocess
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
APP = "/Applications/语雀.app/Contents/MacOS/语雀"
LAUNCHER = os.path.join(HERE, "yuque_launcher.py")


class PipeCDP:
    def __init__(self, extra_args=None, log_path="/tmp/yuque-cdp-app.log"):
        extra = ["--remote-debugging-pipe"] + (extra_args or [])
        c_r, c_w = os.pipe()   # host -> browser
        b_r, b_w = os.pipe()   # browser -> host

        self._logf = open(log_path, "wb")
        self.proc = subprocess.Popen(
            [sys.executable, LAUNCHER, APP, str(c_r), str(b_w)] + extra,
            close_fds=True,
            pass_fds=(c_r, b_w),
            stdin=subprocess.DEVNULL,
            stdout=self._logf,
            stderr=subprocess.STDOUT,
            cwd="/tmp",
        )
        os.close(c_r)
        os.close(b_w)
        self._w = c_w
        self._r = b_r
        self._buf = b""
        self._id = 0
        self._lock = threading.Lock()
        self._replies = {}
        self._events = []
        self._evt_cond = threading.Condition()
        self._reader = threading.Thread(target=self._read_loop, daemon=True)
        self._reader.start()

    # ---------- plumbing ----------
    def _read_loop(self):
        while True:
            try:
                chunk = os.read(self._r, 262144)
            except OSError:
                break
            if not chunk:
                break
            self._buf += chunk
            while b"\0" in self._buf:
                raw, self._buf = self._buf.split(b"\0", 1)
                if not raw.strip():
                    continue
                try:
                    msg = json.loads(raw.decode("utf-8"))
                except Exception:
                    continue
                if "id" in msg:
                    with self._lock:
                        self._replies[msg["id"]] = msg
                else:
                    with self._evt_cond:
                        self._events.append(msg)
                        self._evt_cond.notify_all()
        with self._evt_cond:
            self._evt_cond.notify_all()

    def send(self, method, params=None, session_id=None, timeout=30):
        self._id += 1
        mid = self._id
        msg = {"id": mid, "method": method}
        if params is not None:
            msg["params"] = params
        if session_id:
            msg["sessionId"] = session_id
        os.write(self._w, json.dumps(msg).encode("utf-8") + b"\0")
        deadline = time.time() + timeout
        while time.time() < deadline:
            with self._lock:
                if mid in self._replies:
                    return self._replies.pop(mid)
            time.sleep(0.01)
        raise TimeoutError(f"no reply for {method}")

    def eval(self, expression, session_id, await_promise=True, timeout=90):
        r = self.send("Runtime.evaluate", {
            "expression": expression,
            "returnByValue": True,
            "awaitPromise": await_promise,
            "userGesture": True,
        }, session_id=session_id, timeout=timeout)
        res = r.get("result", {})
        if "exceptionDetails" in res:
            raise RuntimeError(json.dumps(res["exceptionDetails"], ensure_ascii=False)[:3000])
        return res.get("result", {}).get("value")

    def targets(self):
        return self.send("Target.getTargets")["result"]["targetInfos"]

    def attach(self, target_id):
        return self.send("Target.attachToTarget", {"targetId": target_id, "flatten": True})["result"]["sessionId"]

    def close(self):
        try:
            self.proc.terminate()
        except Exception:
            pass
        for fd in (self._w, self._r):
            try:
                os.close(fd)
            except Exception:
                pass
