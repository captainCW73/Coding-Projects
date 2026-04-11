// Simple in‑memory checklist view – transient, no persistence
import SwiftUI

struct CheckItem: Identifiable {
    let id = UUID()
    var title: String
    var isChecked: Bool = false
}

struct ChecklistView: View {
    @State private var items: [CheckItem] = []
    @State private var newItemTitle: String = ""
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        VStack(alignment: .leading) {
            Text("Checklist")
                .font(.headline)
                .padding(.bottom, 4)
            List {
                ForEach($items) { $item in
                    HStack {
                        Toggle(isOn: $item.isChecked) {
                            Text(item.title)
                        }
                    }
                }
                .onDelete(perform: deleteItems)
                HStack {
                    TextField("New item", text: $newItemTitle)
                    Button(action: addItem) {
                        Image(systemName: "plus.circle.fill")
                    }
                    .disabled(newItemTitle.trimmingCharacters(in: .whitespaces).isEmpty)
                }
            }
            .frame(height: 200)
            HStack {
                Spacer()
                Button("Close") { dismiss() }
                    .keyboardShortcut(.cancelAction)
            }
        }
        .padding(8)
        .frame(width: 300)
    }

    private func addItem() {
        let trimmed = newItemTitle.trimmingCharacters(in: .whitespaces)
        guard !trimmed.isEmpty else { return }
        items.append(CheckItem(title: trimmed))
        newItemTitle = ""
    }

    private func deleteItems(at offsets: IndexSet) {
        items.remove(atOffsets: offsets)
    }
}
