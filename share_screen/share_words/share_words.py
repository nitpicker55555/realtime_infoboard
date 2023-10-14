from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

messages = []

@app.route('/')
def index():
    return render_template('index.html', messages=messages)

@app.route('/send', methods=['POST'])
def send():
    text = request.form.get('message')
    if text:
        messages.append(text)
        return jsonify(status="success")
    return jsonify(status="fail")
@app.route('/get_messages_count')
def get_messages_count():
    return jsonify(count=len(messages))

@app.route('/get_messages')
def get_messages():
    return jsonify(messages=messages)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5050)
