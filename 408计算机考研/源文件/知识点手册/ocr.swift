import Foundation
import Vision
import AppKit

// Usage: ocr <image1> [image2 ...]
// Prints "===== <path> =====" followed by recognized text, one line per observation (top→bottom).

func ocr(path: String) -> String {
    guard let img = NSImage(contentsOfFile: path),
          let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        return "[ERROR] cannot load \(path)"
    }
    let request = VNRecognizeTextRequest()
    request.recognitionLevel = .accurate
    request.usesLanguageCorrection = true
    request.recognitionLanguages = ["zh-Hans", "en-US"]
    if #available(macOS 13.0, *) {
        request.automaticallyDetectsLanguage = false
    }
    let handler = VNImageRequestHandler(cgImage: cg, options: [:])
    do {
        try handler.perform([request])
    } catch {
        return "[ERROR] perform failed: \(error)"
    }
    guard let obs = request.results else { return "" }
    // Vision returns observations roughly in reading order for these documents.
    var lines: [String] = []
    for o in obs {
        if let top = o.topCandidates(1).first {
            lines.append(top.string)
        }
    }
    return lines.joined(separator: "\n")
}

let args = Array(CommandLine.arguments.dropFirst())
if args.isEmpty {
    FileHandle.standardError.write("usage: ocr <image>...\n".data(using: .utf8)!)
    exit(2)
}
for p in args {
    print("===== \(p) =====")
    print(ocr(path: p))
    print("")
}
