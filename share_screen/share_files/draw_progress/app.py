from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import datetime
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('message_from_client')
def handle_message(data):
    ip = request.remote_addr
    timestamp = datetime.datetime.now()
    timestamp += datetime.timedelta(hours=2)
    formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')

    message_content = f"{formatted_timestamp} {ip} '{data['message']}'"
    match = re.search(r'\[(\d+)%\] (.*\.jsonl)', data['message'])

    if match:
        percentage = int(match.group(1))
        filename = match.group(2)
        emit('update_progress', {'percentage': percentage, 'filename': filename}, broadcast=True)
    else:
        emit('message_from_server', {'message': message_content}, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)
