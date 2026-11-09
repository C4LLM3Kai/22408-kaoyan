import Foundation
import PDFKit

let args = CommandLine.arguments
guard let doc = PDFDocument(url: URL(fileURLWithPath: args[1])) else { fatalError("no pdf") }
var out = ""
for i in 0..<doc.pageCount {
    let text = doc.page(at: i)?.string ?? ""
    out += "===== PAGE \(i + 1) =====\n" + text + "\n"
}
try out.write(toFile: args[2], atomically: true, encoding: .utf8)
print("pages:", doc.pageCount)
