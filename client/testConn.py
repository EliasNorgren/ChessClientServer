import asyncio
import websockets
import threading
import tkinter as tk

import signal
import time
import sys

ws = None

# Define a signal handler function


def handler(signum, frame):
    print(f"Received signal {signum}")
    websocket_thread.join()

# Register the signal handler for SIGINT (Ctrl+C)


async def receive_messages():
    global ws
    async with websockets.connect("ws://localhost:8080") as websocket:
        ws = websocket
        print("Connected")
        await websocket.send("create room 1337")
        try:
            while True:
                message = await websocket.recv()
                print(f"Received: {message}")
        except websockets.exceptions.ConnectionClosedOK:
            print("Connection closed gracefully by the server")


def buttonClick():
    global ws, input
    if ws:
        asyncio.get_event_loop().run_until_complete(ws.send(input.get()))


# Create a thread for WebSocket communication
websocket_thread = threading.Thread(
    target=lambda: asyncio.run(receive_messages()))

input = None

if __name__ == "__main__":

    # signal.signal(signal.SIGINT, handler)

    # Start the WebSocket thread
    websocket_thread.start()

    # asyncio.get_event_loop().run_until_complete(receive_messages())

    # Create the main application window
    root = tk.Tk()
    root.title("WebSocket Client")

    # Create a button and associate it with the buttonClick function
    button = tk.Button(root, text="Send Message", command=buttonClick)
    input = tk.Entry(root)
    input.pack()
    button.pack()

    # Start the Tkinter main event loop
    root.mainloop()
