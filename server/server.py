from chessEngine import chessEngine
import websockets
import asyncio
from websockets.server import serve


class server:
    def __init__(self, port: int) -> None:
        print("Running server!")
        self.roomNumberToWebsocketTable = {}
        self.websocketToRoomnumberTable = {}
        self.roomNumberToChessEngine = {}
        self.whiteForRoom = {}
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
            self.whiteForRoom[roomNumber] = websocket
            await websocket.send(f"Created room {roomNumber}")

        else:
            self.roomNumberToWebsocketTable[roomNumber].append(websocket)
            self.websocketToRoomnumberTable[websocket] = roomNumber
            await websocket.send(f"Successfully joined room {roomNumber}")

            engineForRoom = chessEngine()
            self.roomNumberToChessEngine[roomNumber] = engineForRoom

        # -------------------------------------

        try:
            while True:
                message = await websocket.recv()
                roomNumber = self.websocketToRoomnumberTable[websocket]
                print(f"Incomming message in room {roomNumber} :" + message)
                message = message.split(" ")

                if message[0] == "move":
                    eng: chessEngine = self.roomNumberToChessEngine[roomNumber]

                    playerIsWhite = self.whiteForRoom[roomNumber] == websocket
                    if (playerIsWhite and not eng.whitesTurn()) or (not playerIsWhite and eng.whitesTurn()):
                        await websocket.send("Not your turn")
                        continue

                    if not eng.moveIsLegal(message[1]):
                        await websocket.send("Illegal move")
                        continue

                    eng.performMove(message[1])

                    if eng.gameIsCheckMate():
                        won = ""
                        if eng.whitesTurn():
                            won = "white"
                        else:
                            won = "black"
                        result = f"Game is checkmate {won} won!"
                        await self.roomNumberToWebsocketTable[roomNumber][0].send(result)
                        await self.roomNumberToWebsocketTable[roomNumber][1].send(result)
                        continue
                        # Continue??

                    fen = eng.getFen()

                    print(f"Sending new board after move {message[0]}")
                    await self.roomNumberToWebsocketTable[roomNumber][0].send(fen)
                    await self.roomNumberToWebsocketTable[roomNumber][1].send(fen)
                else:
                    await websocket.send("Unknown command")

        except websockets.exceptions.ConnectionClosedOK:
            print("Connection closed gracefully by the client")
        finally:
            print("Closing connection")
            # self.clients.remove(websocket)
