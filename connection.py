import asyncio
from typing import Dict
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.websockets import WebSocketState

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.lock = asyncio.Lock()  # Ensuring thread safety in case of concurrent access

    async def connect(self, websocket: WebSocket, session_id: str):
        """Accept a WebSocket connection and store it with its session ID."""
        await websocket.accept()
        async with self.lock:
            self.active_connections[session_id] = websocket
        print(f"Session {session_id} connected.")

    async def disconnect(self, session_id: str):
        """Remove the WebSocket connection for the given session ID."""
        async with self.lock:
            if session_id in self.active_connections:
                del self.active_connections[session_id]
                print(f"Session {session_id} disconnected.")

    async def send_personal_message(self, message: str, session_id: str):
        """Send a message to a specific client identified by session ID without blocking."""
        async with self.lock:
            websocket = self.active_connections.get(session_id)
        
        if websocket and websocket.client_state == WebSocketState.CONNECTED:
            asyncio.create_task(self._safe_send(websocket, message, session_id))
        else:
            print(f'Websocket {session_id} is disconnected')

    async def broadcast(self, message: str):
        """Broadcast a message to all connected clients without blocking."""
        async with self.lock:
            connections = list(self.active_connections.items())

        for session_id, websocket in connections:
            if(websocket.client_state == WebSocketState.CONNECTED):
                asyncio.create_task(self._safe_send(websocket, message, session_id))
            else:
                print(f'Websocket {session_id} is disconnected')

    async def _safe_send(self, websocket: WebSocket, message: str, session_id: str):
        """Safely send a message, handling disconnects."""
        try:
            await websocket.send_text(message)
        except WebSocketDisconnect:
            print(f"Session {session_id} disconnected unexpectedly.")
            await self.disconnect(session_id)

    async def receive_message(self, session_id: str) -> str:
        """Receive a message from a specific client identified by session ID."""
        async with self.lock:
            websocket = self.active_connections.get(session_id)
        
        if websocket:
            return await websocket.receive_text()
        else:
            raise ValueError(f"No active connection found for session {session_id}")
