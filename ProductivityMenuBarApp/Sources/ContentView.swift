// Main menu‑bar UI composition
import SwiftUI

struct ContentView: View {
    @EnvironmentObject private var pomodoro: PomodoroTimer
    @EnvironmentObject private var dndController: DNDController
    @EnvironmentObject private var calendarProvider: CalendarProvider
    @EnvironmentObject private var notificationManager: NotificationManager
    @State private var showNotes = false
    @State private var showChecklist = false
    @State private var showSettings = false

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            // Pomodoro section
            pomodoroSection
            Divider()
            // DND toggle
            Toggle("Do Not Disturb", isOn: $dndController.isEnabled)
                .onChange(of: dndController.isEnabled) { _ in dndController.toggle() }
            Divider()
            // Quick notes button
            Button(action: { showNotes.toggle() }) {
                Label("Quick Notes", systemImage: "note.text")
            }
            .sheet(isPresented: $showNotes) { QuickNotesView() }
            // Checklist button
            Button(action: { showChecklist.toggle() }) {
                Label("Checklist", systemImage: "checklist")
            }
            .sheet(isPresented: $showChecklist) { ChecklistView() }
            Divider()
            // Calendar events
            if !calendarProvider.upcomingEvents.isEmpty {
                Text("Upcoming Events")
                    .font(.subheadline)
                ForEach(calendarProvider.upcomingEvents) { event in
                    HStack {
                        Text(event.title)
                            .lineLimit(1)
                        Spacer()
                        Text(event.startDate, style: .time)
                    }
                }
            }
            Divider()
            // Settings button
            Button(action: { showSettings.toggle() }) {
                Label("Settings", systemImage: "gearshape")
            }
            .sheet(isPresented: $showSettings) { SettingsView() }
        }
        .padding(12)
        .frame(width: 300)
    }

    private var pomodoroSection: some View {
        VStack(alignment: .leading) {
            Text(pomodoro.currentPhase.rawValue.capitalized)
                .font(.headline)
            Text(timeString(from: pomodoro.timeRemaining))
                .font(.system(size: 32, weight: .bold, design: .monospaced))
            HStack {
                if pomodoro.currentPhase == .stopped {
                    Button("Start") { pomodoro.start() }
                } else {
                    Button(pomodoro.isRunning ? "Pause" : "Start") {
                        pomodoro.timerCancellable == nil ? pomodoro.start() : pomodoro.pause()
                    }
                    Button("Reset") { pomodoro.reset() }
                }
            }
        }
    }

    private func timeString(from seconds: Double) -> String {
        let intSec = Int(seconds)
        let mins = intSec / 60
        let secs = intSec % 60
        return String(format: "%02d:%02d", mins, secs)
    }
}
