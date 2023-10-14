from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
import datetime,re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'  # Using SQLite for simplicity
socketio = SocketIO(app, cors_allowed_origins="*")
db = SQLAlchemy(app)

# Define the Message model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500))

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message_from_client')
def handle_message(data):
    ip = request.remote_addr
    timestamp = datetime.datetime.now()

    # 增加2小时
    timestamp += datetime.timedelta(hours=2)

    # 将时间格式化为字符串
    formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    message_content = f" {formatted_timestamp} {ip} '{data['message']}'  "
    message = Message(content=message_content)
    db.session.add(message)
    db.session.commit()  # store the message in database
    emit('message_from_server', {'message': message_content}, broadcast=True)


@socketio.on('get_all_dates')
def send_all_dates():
    messages = Message.query.all()

    date_pattern = re.compile(r"\d{4}-\d{2}-\d{2}")  # Matches YYYY-MM-DD
    dates = list(set([date_pattern.search(message.content).group(0) for message in messages if
                      date_pattern.search(message.content)]))

    emit('dates_from_server', {'dates': dates})

@socketio.on('get_all_files')
def send_all_files():
    messages = Message.query.all()

    date_pattern  = re.compile(r"'([\d-]+_[\d-]+_.*?\.jsonl)'")

    dates = list(set([date_pattern.search(message.content).group(0) for message in messages if
                      date_pattern.search(message.content)]))

    emit('files_from_server', {'files': dates})
@socketio.on('get_all_messages')
def send_all_messages():
    all_messages = Message.query.all()
    for message in all_messages:
        emit('message_from_server', {'message': message.content})


@socketio.on('get_all_ips')
def send_all_ips():
    messages = Message.query.all()

    ip_pattern = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")  # Matches IP address
    ips = list(set([ip_pattern.search(message.content).group(0) for message in messages if
                    ip_pattern.search(message.content)]))

    emit('ips_from_server', {'ips': ips})
@socketio.on('clear_all_messages')
def clear_all_messages():
    Message.query.delete()  # Delete all messages from the database
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This will create messages.db with the necessary tables
    socketio.run(app, host='0.0.0.0',port=8855,debug=True, allow_unsafe_werkzeug=True)