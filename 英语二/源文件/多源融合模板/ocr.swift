import Foundation
import CoreGraphics
import Vision
let args=CommandLine.arguments
let url=URL(fileURLWithPath:args[1])
guard let doc=CGPDFDocument(url as CFURL) else {fatalError("Cannot read PDF")}
let start=Int(args[2])!, end=Int(args[3])!
var output=""
for number in start...end {
 autoreleasepool {
 guard let page=doc.page(at:number) else{return}
 let box=page.getBoxRect(.mediaBox)
 let scale=min(2.8,2100/box.width)
 let width=Int(box.width*scale),height=Int(box.height*scale)
 guard let ctx=CGContext(data:nil,width:width,height:height,bitsPerComponent:8,bytesPerRow:width*4,space:CGColorSpaceCreateDeviceRGB(),bitmapInfo:CGImageAlphaInfo.premultipliedLast.rawValue) else{return}
 ctx.setFillColor(CGColor(gray:1,alpha:1));ctx.fill(CGRect(x:0,y:0,width:width,height:height))
 ctx.scaleBy(x:scale,y:scale);ctx.translateBy(x:-box.minX,y:-box.minY);ctx.drawPDFPage(page)
 guard let img=ctx.makeImage() else{return}
 let request=VNRecognizeTextRequest()
 request.recognitionLevel = .accurate
 request.recognitionLanguages=["zh-Hans","en-US"]
 request.usesLanguageCorrection=true
 request.automaticallyDetectsLanguage=true
 do {
  try VNImageRequestHandler(cgImage:img,options:[:]).perform([request])
  let lines=(request.results ?? []).compactMap{$0.topCandidates(1).first?.string}
  output += "===== PAGE \(number) =====\n"+lines.joined(separator:"\n")+"\n"
 } catch {output += "===== PAGE \(number) =====\n[OCR ERROR: \(error)]\n"}
 }
}
try output.write(toFile:args[4],atomically:true,encoding:.utf8)
