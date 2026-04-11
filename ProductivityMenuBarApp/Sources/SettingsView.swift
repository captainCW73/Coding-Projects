// Settings view to adjust Pomodoro intervals
import SwiftUI

struct SettingsView: View {
    @EnvironmentObject private var pomodoro: PomodoroTimer
    @State private var workMinutes: Double = 25
    @State private var shortBreakMinutes: Double = 5
    @State private var longBreakMinutes: Double = 10
    @State private var cyclesBeforeLong: Int = 4

    var body: some View {
        Form {
            Section(header: Text("Pomodoro Durations")) {
                HStack {
                    Text("Work")
                    Spacer()
                    Slider(value: $workMinutes, in: 5...60, step: 1)
                    Text("\(Int(workMinutes)) min")
                }
                HStack {
                    Text("Short Break")
                    Spacer()
                    Slider(value: $shortBreakMinutes, in: 1...30, step: 1)
                    Text("\(Int(shortBreakMinutes)) min")
                }
                HStack {
                    Text("Long Break")
                    Spacer()
                    Slider(value: $longBreakMinutes, in: 5...30, step: 1)
                    Text("\(Int(longBreakMinutes)) min")
                }
                HStack {
                    Text("Cycles before Long Break")
                    Spacer()
                    Stepper(value: $cyclesBeforeLong, in: 1...10) {
                        Text("\(cyclesBeforeLong)")
                    }
                }
            }
            Button("Save") {
                pomodoro.workDuration = workMinutes * 60
                pomodoro.shortBreakDuration = shortBreakMinutes * 60
                pomodoro.longBreakDuration = longBreakMinutes * 60
                pomodoro.cyclesBeforeLongBreak = cyclesBeforeLong
                // Reset timer to apply new settings immediately
                pomodoro.reset()
            }
        }
        .frame(width: 350, height: 250)
        .onAppear {
            // Load current values from pomodoro
            workMinutes = pomodoro.workDuration / 60
            shortBreakMinutes = pomodoro.shortBreakDuration / 60
            longBreakMinutes = pomodoro.longBreakDuration / 60
            cyclesBeforeLong = pomodoro.cyclesBeforeLongBreak
        }
    }
}
