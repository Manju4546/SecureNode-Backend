import asyncio
import websockets
import json
import os

connected_nodes = {}

async def handler(websocket):
    node_id = None
    try:
        async for message in websocket:
            data = json.loads(message)
            action = data.get("action")

            if action == "register":
                node_id = data.get("id")
                connected_nodes[node_id] = websocket
                print(f"🟢 Node Registered: {node_id}")

            elif action == "route":
                target_id = data.get("target")
                payload = data.get("payload")
                if target_id in connected_nodes:
                    target_ws = connected_nodes[target_id]
                    await target_ws.send(json.dumps({
                        "action": "incoming",
                        "sender": node_id,
                        "payload": payload
                    }))
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        if node_id in connected_nodes:
            del connected_nodes[node_id]
            print(f"🔴 Node Disconnected: {node_id}")

async def main():
    # CRITICAL RENDER UPGRADE: Bind to 0.0.0.0 and listen for Render's dynamic PORT
    port = int(os.environ.get("PORT", 8765))
    async with websockets.serve(handler, "0.0.0.0", port):
        print(f"🚀 Cloud Signaling Server running on port {port}")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())