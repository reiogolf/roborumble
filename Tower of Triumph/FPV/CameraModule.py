from picamera2 import Picamera2
import io
from PIL import Image

picam2 = Picamera2()


def startCameraAndGetImage():
    picam2.start()
    data = io.BytesIO()
    picam2.capture_file(data, format='jpeg')
    img = Image.open(data)
    picam2.stop()
    return img
