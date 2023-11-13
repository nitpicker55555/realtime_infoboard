from flask import Flask, render_template, send_from_directory, request
import socket

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/capture', methods=["POST"])
def capture():
    UDP_IP = "10.181.210.246"  # PC的IP
    UDP_PORT = 9999
    MESSAGE = "capture"

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))

    data, addr = sock.recvfrom(655070000)
    with open("screenshot.png", "wb") as f:
        f.write(data)

    return send_from_directory('.', "screenshot.png", as_attachment=False)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=9999,debug=True)
