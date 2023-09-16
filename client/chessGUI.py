import tkinter as tk


class ChessGUI:

    def startGUI(self):
        # Create the main application window
        self.root = tk.Tk()
        self.root.title("WebSocket Client")

        # Create a button and associate it with the buttonClick function

        self.input = tk.Entry(self.root)
        self.input.pack()
        self.button = tk.Button(
            self.root, text="Send Message", command=lambda: self.buttonClick(self.input.get()))
        self.button.pack()

        # Start the Tkinter main event loop
        self.root.mainloop()
#  command=lambda: self.__loginHandler(usernameEntry.get())
