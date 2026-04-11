// swift-tools-version:5.8
import PackageDescription

let package = Package(
    name: "ProductivityMenuBarApp",
    platforms: [
        .macOS(.v13)
    ],
    products: [
        .executable(name: "ProductivityMenuBarApp", targets: ["ProductivityMenuBarApp"])
    ],
    dependencies: [],
    targets: [
        .executableTarget(
            name: "ProductivityMenuBarApp",
            dependencies: [],
            path: "Sources",
            resources: [.process("../Resources")]
        )
    ]
)
