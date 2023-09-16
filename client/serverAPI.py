import threading
import asyncio
import websockets


class ServerAPI:
    def __init__(self, ip, port, roomNumber) -> None:
        self.ip = ip
        self.port = port
        self.roomNumber = roomNumber
        self.websocket_thread = threading.Thread(
            target=lambda: asyncio.run(self.handleMessages()))

    async def handleMessages(self):
        async with websockets.connect(f"ws://{self.ip}:{self.port}") as websocket:
            self.ws = websocket
            print("Connected")
            await websocket.send(f"create room {self.roomNumber}")
            status = await websocket.recv()
            print(f"Status:{status}")
            if status == "Room full":
                print("Room was full")
                await websocket.close()
                return
            if "created room" in status:
                self.playingAsWhite = True
            if "joined room" in status:
                self.playingAsWhite = False
            try:
                while True:
                    message = await websocket.recv()
                    print(f"Received: {message}")

                    if "checkmate" in message:
                        await websocket.close()
                    if "fen" in message:
                        self.handleReceivedFEN(message.split(" ")[1])
            except websockets.exceptions.ConnectionClosedOK:
                print("Connection closed gracefully by the server")

    def startConnection(self):
        self.websocket_thread.start()

    def sendMessage(self, message):
        if self.ws:
            asyncio.get_event_loop().run_until_complete(self.ws.send(message))
