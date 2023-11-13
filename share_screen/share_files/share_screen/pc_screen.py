import socket
import pyautogui
import io
from PIL import Image

UDP_IP = "10.181.210.246"  # 服务器的IP
UDP_PORT = 9999
BUFFER_SIZE = 655070000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(BUFFER_SIZE)
    if data.decode() == "capture":
        screenshot = pyautogui.screenshot()
        img_byte_arr = io.BytesIO()
        screenshot.save(img_byte_arr, format='PNG')
        byte_image = img_byte_arr.getvalue()
        sock.sendto(byte_image, addr)
