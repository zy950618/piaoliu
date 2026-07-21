from collections import defaultdict

from fastapi import WebSocket


class RealtimeHub:
    def __init__(self) -> None:
        self._connections: dict[str, dict[str, set[WebSocket]]] = defaultdict(lambda: defaultdict(set))

    async def connect(self, conversation_id: str, user_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections[conversation_id][user_id].add(websocket)

    def disconnect(self, conversation_id: str, user_id: str, websocket: WebSocket) -> None:
        users = self._connections.get(conversation_id)
        if users is None:
            return
        sockets = users.get(user_id)
        if sockets is not None:
            sockets.discard(websocket)
            if not sockets:
                users.pop(user_id, None)
        if not users:
            self._connections.pop(conversation_id, None)

    async def broadcast(self, conversation_id: str, event: dict) -> None:
        users = self._connections.get(conversation_id, {})
        stale: list[tuple[str, WebSocket]] = []
        for user_id, sockets in list(users.items()):
            for websocket in list(sockets):
                try:
                    await websocket.send_json(event)
                except RuntimeError:
                    stale.append((user_id, websocket))
        for user_id, websocket in stale:
            self.disconnect(conversation_id, user_id, websocket)


realtime_hub = RealtimeHub()
