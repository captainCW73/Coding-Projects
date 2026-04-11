// Calendar provider – read‑only access to upcoming events using EventKit
import Foundation
import EventKit
import SwiftUI

class CalendarProvider: ObservableObject {
    @Published var upcomingEvents: [SimpleEvent] = []
    private let store = EKEventStore()

    struct SimpleEvent: Identifiable {
        let id = UUID()
        let title: String
        let startDate: Date
    }

    init() {
        requestAccessAndLoad()
    }

    private func requestAccessAndLoad() {
        store.requestAccess(to: .event) { granted, _ in
            if granted {
                self.loadUpcoming()
            } else {
                // Permission denied – keep list empty
                DispatchQueue.main.async {
                    self.upcomingEvents = []
                }
            }
        }
    }

    private func loadUpcoming() {
        let calendars = store.calendars(for: .event)
        let now = Date()
        let oneWeekLater = Calendar.current.date(byAdding: .day, value: 7, to: now)!
        let predicate = store.predicateForEvents(withStart: now, end: oneWeekLater, calendars: calendars)
        let events = store.events(matching: predicate)
            .sorted { $0.startDate < $1.startDate }
            .prefix(5)
        let simple = events.map { SimpleEvent(title: $0.title, startDate: $0.startDate) }
        DispatchQueue.main.async {
            self.upcomingEvents = Array(simple)
        }
    }
}
