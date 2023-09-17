import tkinter as tk


class RoomSelectorGUI:

    def startGUI(self, root):

        root.title("RoomSelector")
        self.entry = tk.Entry(root)
        self.entry.pack()
        self.button = tk.Button(
            root, command=lambda: self.joinOrCreateServer(self.entry.get()), text="Button")
        self.button.pack()
