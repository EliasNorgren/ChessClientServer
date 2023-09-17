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
            self.handle_client_connection, "", port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    async def handle_client_connection(self, websocket, path):

        print(f"Incoming connection: {websocket.remote_address}")

        # Receive room # ----- "create room x" or "join room x"
        message = await websocket.recv()
        # Send ack of room created
        roomNumber = message.split(" ")[2]
        playingAs = message.split(" ")[3]
        print(f"Pre setup message:{message}")
        print(f"roomNr={roomNumber}, playingAs={playingAs}")
        if roomNumber not in self.roomNumberToWebsocketTable:
            newList = []
            newList.append(websocket)
            self.websocketToRoomnumberTable[websocket] = roomNumber
            self.roomNumberToWebsocketTable[roomNumber] = newList
            if playingAs == "white":
                self.whiteForRoom[roomNumber] = websocket

            print(f"Room {roomNumber} created.")
            await websocket.send(f"Created room {roomNumber}")

        elif len(self.roomNumberToWebsocketTable[roomNumber]) == 1:
            if playingAs == "white":
                self.whiteForRoom[roomNumber] = websocket
            self.roomNumberToWebsocketTable[roomNumber].append(websocket)
            self.websocketToRoomnumberTable[websocket] = roomNumber

            engineForRoom = chessEngine()
            self.roomNumberToChessEngine[roomNumber] = engineForRoom
            await websocket.send(f"Successfully joined room {roomNumber}")

        else:
            print("Cant join, full.")
            await websocket.send("Room full")

        # -------------------------------------

        try:
            while True:
                message = await websocket.recv()
                roomNumber = self.websocketToRoomnumberTable[websocket]
                print(f"Incomming message in room {roomNumber} :" + message)
                message = message.split(" ")

                if message[0] == "move":

                    if len(self.websocketToRoomnumberTable[websocket]) < 2:
                        await websocket.send("game not started")
                        continue

                    eng: chessEngine = self.roomNumberToChessEngine[roomNumber]
                    playerIsWhite = self.whiteForRoom[roomNumber] == websocket
                    print(f"PlayerIsWhite: {playerIsWhite}")
                    if (playerIsWhite and not eng.whitesTurn()) or (not playerIsWhite and eng.whitesTurn()):
                        await websocket.send("Not your turn")
                        continue

                    if not eng.moveIsLegal(message[1]):
                        await websocket.send("Illegal move")
                        continue

                    eng.performMove(message[1])

                    fen = eng.getFen()

                    print(f"Sending new board after move {message[1]}")
                    await self.roomNumberToWebsocketTable[roomNumber][0].send("fen " + fen)
                    await self.roomNumberToWebsocketTable[roomNumber][1].send("fen " + fen)

                    if eng.gameIsCheckMate():

                        won = ""
                        if eng.whitesTurn():
                            won = "white"
                        else:
                            won = "black"
                        result = f"Game is checkmate {won} won!"
                        await self.roomNumberToWebsocketTable[roomNumber][0].send(result)
                        await self.roomNumberToWebsocketTable[roomNumber][1].send(result)

                        ws1 = self.roomNumberToWebsocketTable[roomNumber][0]
                        ws2 = self.roomNumberToWebsocketTable[roomNumber][1]
                        del (self.websocketToRoomnumberTable[ws1])
                        del (self.websocketToRoomnumberTable[ws2])

                        del (self.roomNumberToChessEngine[roomNumber])
                        del (self.whiteForRoom[roomNumber])
                        del (self.roomNumberToWebsocketTable[roomNumber])

                else:
                    await websocket.send("Unknown command")

        except websockets.exceptions.ConnectionClosedOK:
            print("Connection closed gracefully by the client")
        finally:
            print("Closing connection")
            try:
                if roomNumber in self.roomNumberToWebsocketTable:
                    websocketsList = self.roomNumberToWebsocketTable[roomNumber]
                    for ws in websocketsList:
                        del (self.websocketToRoomnumberTable[ws])
                    del self.roomNumberToWebsocketTable[roomNumber]

                if roomNumber in self.whiteForRoom:
                    del self.whiteForRoom[roomNumber]
                if roomNumber in self.roomNumberToChessEngine:
                    del self.roomNumberToChessEngine[roomNumber]

            except KeyError:
                pass
                # self.clients.remove(websocket)
