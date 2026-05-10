from fastapi import WebSocket

# Observer pattern implementation for managing websocket connections

class WebSocketManager:

    # mapper from reservation_id to websocket connection
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}



    # function to connect a websocket to a reservation
    async def connect(self , reservation_id:str , websocket:WebSocket):
        await websocket.accept()
        self.active_connections[reservation_id] = websocket
        print(f"User connected to reservation {reservation_id}")



   # function to disconnect a websocket from a reservation
    def disconnect(self , reservation_id:str):
        if reservation_id in self.active_connections:
            del self.active_connections[reservation_id]
            print(f"User disconnected from reservation {reservation_id}")



   # function to notify a user about the update of their reservation
    async def notify_user(self, reservation_id:str , data:dict):
        if reservation_id in self.active_connections:
            websocket = self.active_connections[reservation_id]
            await websocket.send_json(data)
            print(f"Notification sent to user for reservation {reservation_id}")

ws_manager = WebSocketManager()
    