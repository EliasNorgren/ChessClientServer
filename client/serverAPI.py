import threading
import asyncio
import websockets


class ServerAPI:
    def __init__(self, ip, port) -> None:
        self.ip = ip
        self.port = port
        self.waitForMessageEvent = threading.Event()
        self.websocket_thread = threading.Thread(
            target=lambda: asyncio.run(self.handleMessages()))
        self.connectedToServerEvent = threading.Event()

    async def handleMessages(self):
        async with websockets.connect(f"ws://{self.ip}:{self.port}") as websocket:
            self.ws = websocket
            print("Connected")
            self.connectedToServerEvent.set()
            # await websocket.send(f"create room {self.roomNumber}")
            # status = await websocket.recv()
            # print(f"Status:{status}")

            try:
                while True:
                    message = await websocket.recv()
                    print(f"Received: {message}")

                    if message == "Room full":
                        print("Room was full")
                        await websocket.close()
                        return
                    if message.split(" ")[0] == "Created":
                        # self.playingAsWhite = True
                        self.roomNumber = message.split(" ")[-1]
                        print(f"Created room {self.roomNumber}")

                    if message.split(" ")[0] == "Successfully":
                        # self.playingAsWhite = False
                        self.roomNumber = message.split(" ")[-1]
                        print(f"Joined room {self.roomNumber}")

                    if "checkmate" in message:
                        await websocket.close()
                    if "fen" in message:
                        self.handleReceivedFEN(
                            message.split(" ")[1], self.roomNumber)
                    self.waitForMessageEvent.set()

            except websockets.exceptions.ConnectionClosedOK:
                print("Connection closed gracefully by the server")

    def startConnection(self):
        self.websocket_thread.start()

    def sendMessage(self, message):
        if self.ws:
            asyncio.get_event_loop().run_until_complete(self.ws.send(message))

    def waitForMessage(self):
        self.waitForMessageEvent.wait()
