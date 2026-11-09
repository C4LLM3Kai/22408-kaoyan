import Foundation
import CoreGraphics
import ImageIO
import Vision

let args = CommandLine.arguments
let url = URL(fileURLWithPath: args[1])
guard let src = CGImageSourceCreateWithURL(url as CFURL, nil),
      let img = CGImageSourceCreateImageAtIndex(src, 0, nil) else { fatalError("Cannot read image") }
let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.recognitionLanguages = ["zh-Hans", "en-US"]
request.usesLanguageCorrection = true
request.automaticallyDetectsLanguage = true
var out = ""
do {
    try VNImageRequestHandler(cgImage: img, options: [:]).perform([request])
    for obs in (request.results ?? []) {
        guard let c = obs.topCandidates(1).first else { continue }
        let b = obs.boundingBox
        let y = String(format: "%.4f", 1 - b.midY)
        let x = String(format: "%.4f", b.minX)
        out += "[y=\(y) x=\(x)] \(c.string)\n"
    }
} catch { out = "[OCR ERROR: \(error)]\n" }
try out.write(toFile: args[2], atomically: true, encoding: .utf8)
print("lines: \(out.split(separator: "\n").count)")
