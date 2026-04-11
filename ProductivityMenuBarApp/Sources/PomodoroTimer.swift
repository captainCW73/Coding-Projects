// Pomodoro timer model
import Foundation
import Combine
import SwiftUI

class PomodoroTimer: ObservableObject {
    // Default durations (seconds)
    @AppStorage("workDuration") var workDuration: Double = 25 * 60
    @AppStorage("shortBreakDuration") var shortBreakDuration: Double = 5 * 60
    @AppStorage("longBreakDuration") var longBreakDuration: Double = 10 * 60
    @AppStorage("cyclesBeforeLongBreak") var cyclesBeforeLongBreak: Int = 4

    enum Phase: String {
        case work, shortBreak, longBreak, stopped
    }

    @Published var timeRemaining: Double = 0
    @Published var currentPhase: Phase = .stopped
    @Published var completedCycles: Int = 0

    private var timerCancellable: AnyCancellable?
    var isRunning: Bool { timerCancellable != nil }

    init() {
        // start in stopped state
        reset()
    }

    func start() {
        guard currentPhase != .stopped else { currentPhase = .work }
        scheduleTimer()
    }

    func pause() {
        timerCancellable?.cancel()
    }

    func reset() {
        pause()
        currentPhase = .stopped
        completedCycles = 0
        timeRemaining = workDuration
    }

    private func scheduleTimer() {
        timerCancellable?.cancel()
        timerCancellable = Timer.publish(every: 1, on: .main, in: .common)
            .autoconnect()
            .sink { [weak self] _ in
                self?.tick()
            }
    }

    private func tick() {
        guard timeRemaining > 0 else {
            transitionPhase()
            return
        }
        timeRemaining -= 1
    }

    private func transitionPhase() {
        pause()
        switch currentPhase {
        case .work:
            completedCycles += 1
            if completedCycles % cyclesBeforeLongBreak == 0 {
                currentPhase = .longBreak
                timeRemaining = longBreakDuration
            } else {
                currentPhase = .shortBreak
                timeRemaining = shortBreakDuration
            }
        case .shortBreak, .longBreak:
            currentPhase = .work
            timeRemaining = workDuration
        default:
            break
        }
        // Notify after transition
        NotificationCenter.default.post(name: .pomodoroPhaseChanged, object: self)
        // Restart timer for the new phase
        scheduleTimer()
    }
}

extension Notification.Name {
    static let pomodoroPhaseChanged = Notification.Name("PomodoroPhaseChanged")
}
