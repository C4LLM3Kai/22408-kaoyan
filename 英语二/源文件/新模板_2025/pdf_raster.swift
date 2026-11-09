import Foundation
import PDFKit
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers

let args = CommandLine.arguments
guard let doc = PDFDocument(url: URL(fileURLWithPath: args[1])) else { fatalError("no pdf") }
let pageIndex = Int(args[2])!
let outPath = args[3]
let scale: CGFloat = 2.0

guard let page = doc.page(at: pageIndex) else { fatalError("no page") }
let box = page.bounds(for: .mediaBox)
let w = Int(box.width * scale), h = Int(box.height * scale)
let cs = CGColorSpaceCreateDeviceRGB()
guard let ctx = CGContext(data: nil, width: w, height: h, bitsPerComponent: 8, bytesPerRow: w * 4,
                          space: cs, bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue) else { fatalError("ctx") }
ctx.setFillColor(CGColor(red: 1, green: 1, blue: 1, alpha: 1))
ctx.fill(CGRect(x: 0, y: 0, width: CGFloat(w), height: CGFloat(h)))
ctx.scaleBy(x: scale, y: scale)
guard let cgPage = page.pageRef else { fatalError("no cgpage") }
ctx.drawPDFPage(cgPage)
guard let img = ctx.makeImage() else { fatalError("img") }

let url = URL(fileURLWithPath: outPath)
guard let dst = CGImageDestinationCreateWithURL(url as CFURL, UTType.png.identifier as CFString, 1, nil) else { fatalError("dst") }
CGImageDestinationAddImage(dst, img, nil)
CGImageDestinationFinalize(dst)

// 采样：统计上 12% 区域的高频颜色 + 该区域内近白像素比例
guard let data = ctx.data else { fatalError("data") }
let px = data.bindMemory(to: UInt8.self, capacity: w * h * 4)
var hist: [String: Int] = [:]
var whites = 0, total = 0
let topRows = Int(Double(h) * 0.12)
for y in 0..<topRows {
    for x in 0..<w {
        let i = ((h - 1 - y) * w + x) * 4
        let r = px[i], g = px[i + 1], b = px[i + 2]
        total += 1
        if r > 235 && g > 235 && b > 235 { whites += 1; continue }
        let key = "\(r/8*8),\(g/8*8),\(b/8*8)"
        hist[key, default: 0] += 1
    }
}
let top = hist.sorted { $0.value > $1.value }.prefix(3)
print("page \(pageIndex + 1)  size \(w)x\(h)")
for (k, v) in top { print("  color \(k)  \(v) px") }
print(String(format: "  near-white ratio in top band: %.2f%%", Double(whites) / Double(total) * 100))
