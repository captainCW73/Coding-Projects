// Quick notes popover – transient UI, no persistence
import SwiftUI

struct QuickNotesView: View {
    @State private var note: String = ""
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        VStack(alignment: .leading) {
            Text("Quick Notes")
                .font(.headline)
                .padding(.bottom, 4)
            TextEditor(text: $note)
                .frame(minHeight: 120)
                .border(Color.gray.opacity(0.5), width: 1)
            HStack {
                Spacer()
                Button("Close") {
                    // Discard note on close (transient)
                    dismiss()
                }
                .keyboardShortcut(.cancelAction)
            }
            .padding(.top, 4)
        }
        .padding(8)
        .frame(width: 300)
    }
}
