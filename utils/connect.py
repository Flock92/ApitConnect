import json
import signal
import pathlib
import asyncio
import websockets
from concurrent.futures import ThreadPoolExecutor


class ApitServer:

    def __init__(self, host: str = "localhost", port: str = 8080) -> None:
        self.client_connections = set()     # Store client connections
        self._host = host                   # Store host data
        self._port = port                   # Store port data
        self._server_task = None            # To store the WebSocket server task
        self.server = None                  # Store WebSocket Server
        self.messages = asyncio.Queue()
    
    async def send_message(self, msg) -> None:
        """Send a message to all connected clients."""
        if self.client_connections:
            try:
                await asyncio.gather(*[websocket.send(json.dumps(msg)) 
                                       for websocket in self.client_connections])
            except websockets.exceptions.ConnectionClosedOK:
                self.client_connections.clear()
                print("connection closed")

    async def fetch_message(self) -> dict:
        """"""
        return await self.messages.get()

    async def handle_connection(self, websocket) -> None:
        """Handle a new WebSocket connection"""
        self.client_connections.add(websocket)
        print(f"New client connected. Total clients: {len(self.client_connections)}")

        try:
            async for msg in websocket:
                # print("Message Recieved: {}".format(msg))
                # await websocket.send(f"Echo: {msg}")
                await self.messages.put(msg)
        except websockets.ConnectionClosed:
            print("Client disconnected")
        except websockets.InvalidMessage:
            print("invalid message")

    async def start_server(self) -> None:
        """Start the Websocket server."""
        self.server = await websockets.serve(self.handle_connection, self._host, self._port)
        print(f"Python WebSocket server started at wss://{self._host}:{self._port}")
        await self.server.wait_closed()

    async def run_server(self) -> None:
        """Run the WebSocket server in the background"""
        self._server_task = asyncio.create_task(self.start_server())

    async def stop_server(self) -> None:
        """Stop the WebSocket server"""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            self.server = None
            print("server closed")
        if self._server_task:
            self._server_task.cancel()
            await self._server_task
            print("WebSocket server stopped")
