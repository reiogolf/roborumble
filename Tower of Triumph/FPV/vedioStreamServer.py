import io
import logging
import socketserver
import cv2

from http import server
from threading import Condition

from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

import numpy as np
import os

PAGE = """\
<html>
<head>
<title>Robo Rumble Live Streaming</title>
</head>
<body>
<h1>Robo Rumble Live Streaming</h1>
<img src="stream.mjpg" width="640" height="480" />
</body>
</html>
"""

# Create a VideoWriter object to write frames to a video file
# The 'XVID' codec is used here, but you can change it as needed
vedioFileName = 'game_video'
vedioFileExtention = '.avi'

current_dir = os.getcwd()
# creating file name to avoid overding
vedioFileFullName = vedioFileName+vedioFileExtention
i=1
while os.path.exists(current_dir+'/'+vedioFileFullName):
    vedioFileFullName = vedioFileName+str(i)+vedioFileExtention
    i = i+1
    print(vedioFileFullName)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_video = cv2.VideoWriter(vedioFileFullName, fourcc, 30.0, (640, 480))

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()


class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            global cap
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    # Write the frame to the video file
                    # Convert the MJPEG frame to a NumPy array
                    np_frame = np.frombuffer(frame, dtype=np.uint8)
                    image = cv2.imdecode(np_frame, cv2.IMREAD_COLOR)
                    output_video.write(image)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

output = StreamingOutput()

def StartStream():
    picam2 = Picamera2()
    picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
    picam2.start_recording(JpegEncoder(), FileOutput(output))

    try:
        address = ('', 8000)
        print(address)
        server = StreamingServer(address, StreamingHandler)
        print(server)
        server.serve_forever()
    finally:
        picam2.stop_recording()

# StartStream()
