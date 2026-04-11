// Main entry point for ProductivityMenuBarApp
import SwiftUI
import Combine
import EventKit
import UserNotifications

@main
struct ProductivityMenuBarApp: App {
    // App-wide objects
    @StateObject private var pomodoro = PomodoroTimer()
    @StateObject private var dndController = DNDController()
    @StateObject private var calendarProvider = CalendarProvider()
    @StateObject private var notificationManager = NotificationManager()

    var body: some Scene {
        // Menu bar extra provides the persistent icon and dropdown UI
        MenuBarExtra("Productivity", systemImage: "timer") {
            ContentView()
                .environmentObject(pomodoro)
                .environmentObject(dndController)
                .environmentObject(calendarProvider)
                .environmentObject(notificationManager)
        }
        // Settings window to adjust Pomodoro intervals
        Settings {
            SettingsView()
                .environmentObject(pomodoro)
        }
    }
}
