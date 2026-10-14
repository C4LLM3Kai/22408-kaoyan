#!/usr/bin/env python3
"""Launcher: place the inherited pipe fds at 3 (read) and 4 (write), then exec the app.

Runs as its own exec'd process so that nothing closes fd 3/4 afterwards
(CPython's subprocess runs close_fds *after* preexec_fn, which closes fds
that preexec_fn created -- so the dup2 must happen here instead).
"""
import os
import sys

app = sys.argv[1]
r = int(sys.argv[2])
w = int(sys.argv[3])
extra = sys.argv[4:]

# Move to high fds first so the two dup2 calls cannot clobber each other.
import fcntl

tr = fcntl.fcntl(r, fcntl.F_DUPFD, 100)
tw = fcntl.fcntl(w, fcntl.F_DUPFD, 100)
os.dup2(tr, 3)
os.dup2(tw, 4)
for fd in (r, w):
    if fd not in (3, 4):
        try:
            os.close(fd)
        except OSError:
            pass
try:
    os.close(tr)
    os.close(tw)
except OSError:
    pass
os.setsid()
os.execv(app, [app] + extra)
