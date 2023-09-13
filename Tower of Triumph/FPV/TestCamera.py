from CameraModule import *
import os

currentPath = os.path.join(os.getcwd(), 'images/')
os.mkdir(currentPath)

file_path = currentPath+"test.jpg"
startCameraAndGetImage().save(file_path)

print("Image saved to: " + file_path)
