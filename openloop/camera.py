"""
Encode and Decode tools for OpenLoop
"""

import cv2
import base64
import numpy as np

def capture(camera):
    return cv2.VideoCapture(camera)

def encode(frame):
    ret, jpeg = cv2.imencode('.jpg', frame)
    binary = jpeg.tobytes()
    return base64.b64encode(binary).decode()

def decode(text : str):
    transl = base64.b64decode(text.encode())
    image = np.asarray(bytearray(transl), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

if __name__ == "__main__":
    camera = capture(0)

    ret, frame = camera.read()
    encoded = encode(frame)
    with open("hey.bjng", "w") as f:
        f.write(encoded)