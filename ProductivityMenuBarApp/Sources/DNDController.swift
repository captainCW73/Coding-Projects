// DND controller using AppleScript to toggle Do Not Disturb
import Foundation
import SwiftUI

class DNDController: ObservableObject {
    @Published var isEnabled: Bool = false
    private let scriptEnable = "tell application \"System Events\" to tell process \"ControlCenter\" to click menu bar item \"Do Not Disturb\""
    private let scriptStatus = "defaults -currentHost read com.apple.notificationcenterui doNotDisturb"

    init() {
        // initialize status on launch
        self.isEnabled = fetchCurrentStatus()
    }

    func toggle() {
        // Execute the AppleScript to toggle DND
        let script = NSAppleScript(source: scriptEnable)
        var errorInfo: NSDictionary?
        script?.executeAndReturnError(&errorInfo)
        // Update local state after toggle
        self.isEnabled.toggle()
    }

    private func fetchCurrentStatus() -> Bool {
        // Read the defaults to get current DND status (macOS 12+ stores it in com.apple.notificationcenterui)
        let task = Process()
        task.launchPath = "/usr/bin/defaults"
        task.arguments = ["-currentHost", "read", "com.apple.notificationcenterui", "doNotDisturb"]
        let pipe = Pipe()
        task.standardOutput = pipe
        do {
            try task.run()
            let data = pipe.fileHandleForReading.readDataToEndOfFile()
            if let output = String(data: data, encoding: .utf8)?.trimmingCharacters(in: .whitespacesAndNewlines) {
                return output == "1"
            }
        } catch {
            // ignore errors, assume disabled
        }
        return false
    }
}
