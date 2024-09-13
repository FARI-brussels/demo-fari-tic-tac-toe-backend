import asyncio
import websockets
import pickle
import struct
from ultralytics import YOLO
from PIL import Image
import io
import numpy as np
import json

# Load the YOLO model
model = YOLO("weights/best.pt")
classNames = ["O", "X", "grid"]



async def handle_client(websocket, path):
    try:
        while True:
            # Receive the image sent by the client
            image_data = await websocket.recv()

            # Convert the binary data to an image
            image = Image.open(io.BytesIO(image_data))

            # Convert image to RGB (if needed)
            image = image.convert("RGB")

            # Convert to NumPy array
            frame = np.array(image)

            # Perform object detection
            results = model(frame, stream=True)
            bboxes = []
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    confidence = round(float(box.conf[0]) * 100, 2)
                    cls = int(box.cls[0])
                    bboxes.append({
                        "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                        "class": classNames[cls], "confidence": confidence
                    })

            # Send bounding boxes as a JSON string
            await websocket.send(json.dumps(bboxes))

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Connection closed")

# Start WebSocket server
async def main():
    async with websockets.serve(handle_client, "0.0.0.0", 8080):
        print("WebSocket server running on ws://0.0.0.0:8080")
        await asyncio.Future()  # Run forever

asyncio.run(main())