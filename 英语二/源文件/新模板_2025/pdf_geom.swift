import Foundation
import PDFKit

let args = CommandLine.arguments
guard let doc = PDFDocument(url: URL(fileURLWithPath: args[1])) else { fatalError("no pdf") }
print("page\tminX\tmaxX\tminY\tmaxY\tchars")
for i in 0..<doc.pageCount {
    guard let page = doc.page(at: i) else { continue }
    let box = page.bounds(for: .mediaBox)
    var minX = box.maxX, maxX = 0.0, minY = box.maxY, maxY = 0.0
    let n = page.numberOfCharacters
    var counted = 0
    for c in 0..<n {
        let r = page.characterBounds(at: c)
        if r.width <= 0 || r.height <= 0 { continue }
        minX = min(minX, r.minX); maxX = max(maxX, r.maxX)
        minY = min(minY, r.minY); maxY = max(maxY, r.maxY)
        counted += 1
    }
    print(String(format: "%d\t%.1f\t%.1f\t%.1f\t%.1f\t%d", i + 1, minX, maxX, minY, maxY, counted))
}
