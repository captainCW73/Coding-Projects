// Notification manager – request permission and schedule local notifications
import Foundation
import UserNotifications
import SwiftUI

class NotificationManager: ObservableObject {
    init() {
        requestPermission()
        // Observe pomodoro phase changes to fire notifications
        NotificationCenter.default.addObserver(self, selector: #selector(handlePhaseChange(_:)), name: .pomodoroPhaseChanged, object: nil)
    }

    private func requestPermission() {
        UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .sound]) { granted, _ in
            if granted {
                // nothing else needed
            }
        }
    }

    @objc private func handlePhaseChange(_ notification: Notification) {
        guard let timer = notification.object as? PomodoroTimer else { return }
        let content = UNMutableNotificationContent()
        content.title = "Pomodoro"
        switch timer.currentPhase {
        case .shortBreak:
            content.body = "Time for a short break!"
        case .longBreak:
            content.body = "Long break! Relax."
        case .work:
            content.body = "Back to work!"
        default:
            return
        }
        let trigger = UNTimeIntervalNotificationTrigger(timeInterval: 1, repeats: false)
        let request = UNNotificationRequest(identifier: UUID().uuidString, content: content, trigger: trigger)
        UNUserNotificationCenter.current().add(request, withCompletionHandler: nil)
    }
}
