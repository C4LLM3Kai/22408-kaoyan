import Foundation
import PDFKit
import CoreGraphics

// 行剖面：把每行按颜色分类（teal 填充 / soft 填充 / 白），输出连续区段，
// 用来确认色块是否真的成大块出现、白字是否落在色块里。
let args = CommandLine.arguments
guard let doc = PDFDocument(url: URL(fileURLWithPath: args[1])) else { fatalError("no pdf") }
let pageIndex = Int(args[2])!
let scale: CGFloat = 1.5

guard let page = doc.page(at: pageIndex), let cgPage = page.pageRef else { fatalError("no page") }
let box = page.bounds(for: .mediaBox)
let w = Int(box.width * scale), h = Int(box.height * scale)
guard let ctx = CGContext(data: nil, width: w, height: h, bitsPerComponent: 8, bytesPerRow: w * 4,
                          space: CGColorSpaceCreateDeviceRGB(),
                          bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue) else { fatalError("ctx") }
ctx.setFillColor(CGColor(red: 1, green: 1, blue: 1, alpha: 1))
ctx.fill(CGRect(x: 0, y: 0, width: CGFloat(w), height: CGFloat(h)))
ctx.scaleBy(x: scale, y: scale)
ctx.drawPDFPage(cgPage)

guard let data = ctx.data else { fatalError("data") }
let px = data.bindMemory(to: UInt8.self, capacity: w * h * 4)

func cls(_ i: Int) -> Character {
    let r = Double(px[i]), g = Double(px[i + 1]), b = Double(px[i + 2])
    if abs(r - 14) <= 18 && abs(g - 77) <= 18 && abs(b - 92) <= 18 { return "T" }   // teal
    if abs(r - 242) <= 6 && abs(g - 247) <= 6 && abs(b - 247) <= 6 { return "S" }    // soft
    if r > 240 && g > 240 && b > 240 { return "W" }
    return "d"
}

var runStart = 0
var runCls: Character = " "
var runHas = Set<Character>()
func flush(_ endRow: Int) {
    if runHas.contains("T") || runHas.contains("S") {
        let topPt = Double(runStart) / Double(scale), botPt = Double(endRow) / Double(scale)
        let kinds = runHas.sorted().map(String.init).joined()
        print(String(format: "yTop %6.1f–%6.1f pt  rows %4d  classes=%@", topPt, botPt, endRow - runStart, kinds))
    }
}
var prevCls: Character = " "
for y in 0..<h {
    var counts: [Character: Int] = [:]
    for x in 0..<w {
        let c = cls((y * w + x) * 4)
        counts[c, default: 0] += 1
    }
    let dominant: Character = counts.max { $0.value < $1.value }?.key ?? " "
    if dominant != prevCls {
        flush(y)
        runStart = y
        runHas = []
        prevCls = dominant
    }
    runHas.insert(dominant)
    // 记录该行是否含 teal/soft（即便不是主色）
    if (counts["T"] ?? 0) > 60 { runHas.insert("T") }
    if (counts["S"] ?? 0) > 60 { runHas.insert("S") }
}
flush(h)
