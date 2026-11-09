import AppKit
import PencilKit
import Foundation
let args = CommandLine.arguments
let data = try Data(contentsOf: URL(fileURLWithPath: args[1]))
let drawing = try PKDrawing(data: data)
let bounds = drawing.bounds.insetBy(dx: -4, dy: -4)
let image = drawing.image(from: bounds, scale: 3)
let rep = NSBitmapImageRep(data: image.tiffRepresentation!)!
try rep.representation(using: .png, properties: [:])!.write(to: URL(fileURLWithPath: args[2]))
print("Rendered drawing: \(bounds)")
