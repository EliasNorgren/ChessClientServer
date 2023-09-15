from chessEngine import chessEngine
import websockets
import asyncio
from websockets.server import serve


class server:
    def __init__(self, engine: chessEngine, port: int) -> None:
        print("Running server!")
        self.roomNumberToWebsocketTable = {}
        self.websocketToRoomnumberTable = {}
        self.engine = engine
        start_server = websockets.serve(
            self.handle_client_connection, "localhost", port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    async def handle_client_connection(self, websocket, path):

        address, port, something1, something2 = websocket.remote_address
        print(f"Incoming connection: {address} {port}")

        # Receive room # ----- "create room x" or "join room x"
        message = await websocket.recv()
        # Send ack of room created
        roomNumber = message.split(" ")[2]
        if roomNumber not in self.roomNumberToWebsocketTable:
            newList = []
            newList.append(websocket)
            self.websocketToRoomnumberTable[websocket] = roomNumber
            self.roomNumberToWebsocketTable[roomNumber] = newList
        else:
            self.roomNumberToWebsocketTable[roomNumber].append(websocket)
            self.websocketToRoomnumberTable[websocket] = roomNumber
        await websocket.send(f"Created room {roomNumber}")

        # -------------------------------------

        try:
            while True:
                message = await websocket.recv()
                roomNumber = self.websocketToRoomnumberTable[websocket]
                print(f"Incomming message in room {roomNumber}:" + message)
                message = message.split(" ")

                if message[0] == "move" and self.engine.moveIsLegal(message[1]):
                    self.engine.performMove(message[1])
                    await self.roomNumberToWebsocketTable[roomNumber][0].send(f"done {message[1]}")
                    await self.roomNumberToWebsocketTable[roomNumber][1].send(f"done {message[1]}")

        except websockets.exceptions.ConnectionClosedOK:
            print("Connection closed gracefully by the client")
        finally:
            print("Closing connection")
            # self.clients.remove(websocket)
