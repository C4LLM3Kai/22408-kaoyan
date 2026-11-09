import Foundation
import PDFKit

let args = CommandLine.arguments
let leftLimit = Double(args[2])!
let rightLimit = Double(args[3])!
guard let doc = PDFDocument(url: URL(fileURLWithPath: args[1])) else { fatalError("no pdf") }
for i in 0..<doc.pageCount {
    guard let page = doc.page(at: i) else { continue }
    let text = page.string ?? ""
    let chars = Array(text)
    var offenders: [(Int, String, Double, Double)] = []
    for c in 0..<page.numberOfCharacters where c < chars.count {
        let r = page.characterBounds(at: c)
        if r.width <= 0 || r.height <= 0 { continue }
        if r.minX < leftLimit || r.maxX > rightLimit {
            offenders.append((c, String(chars[c]), r.minX, r.maxX))
        }
    }
    if !offenders.isEmpty {
        print("PAGE \(i + 1): \(offenders.count) out-of-margin chars")
        for o in offenders.prefix(8) {
            print(String(format: "  idx %d  '%@'  x=[%.1f, %.1f]", o.0, o.1, o.2, o.3))
        }
    }
}
