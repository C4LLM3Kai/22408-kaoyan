import Foundation
import PDFKit
import CoreGraphics

let args = CommandLine.arguments
guard let doc = PDFDocument(url: URL(fileURLWithPath: args[1])) else { fatalError("no pdf") }
let pageIndex = Int(args[2])!
let tr = Double(args[3])!, tg = Double(args[4])!, tb = Double(args[5])!
let tol = Double(args.count > 6 ? args[6] : "14")!
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
var count = 0
var minX = w, maxX = 0, minY = h, maxY = 0
for y in 0..<h {
    for x in 0..<w {
        let i = (y * w + x) * 4
        let r = Double(px[i]), g = Double(px[i + 1]), b = Double(px[i + 2])
        if abs(r - tr) <= tol && abs(g - tg) <= tol && abs(b - tb) <= tol {
            count += 1
            minX = min(minX, x); maxX = max(maxX, x)
            minY = min(minY, y); maxY = max(maxY, y)
        }
    }
}
if count == 0 {
    print("page \(pageIndex + 1): target color not found")
} else {
    // 图像坐标系 y 自顶向下
    print(String(format: "page %d: %d px  bbox x=[%.0f,%.0f] y(top-down)=[%.0f,%.0f]  (pt: x=[%.1f,%.1f] yTop=[%.1f,%.1f])",
                 pageIndex + 1, count,
                 Double(minX), Double(maxX), Double(minY), Double(maxY),
                 Double(minX) / Double(scale), Double(maxX) / Double(scale),
                 Double(minY) / Double(scale), Double(maxY) / Double(scale)))
}
