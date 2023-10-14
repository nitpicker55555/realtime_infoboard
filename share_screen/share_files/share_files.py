
import os
from flask import Flask, request, render_template, send_from_directory, redirect,jsonify

from werkzeug.utils import secure_filename

app = Flask(__name__)
messages = []
# 配置文件上传目录
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
# db = SQLAlchemy(app)
# 允许上传的文件类型
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'py'}


@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)




def allowed_file(filename):
    # return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    return True
@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files.get('file')

    if not uploaded_file:
        return "No file uploaded", 400

    if uploaded_file.filename == '':
        return "No file selected", 400
    print(uploaded_file.filename)
    if allowed_file(uploaded_file.filename):
        filename = secure_filename(uploaded_file.filename)
        uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return redirect('/')
    else:
        return "File type not allowed", 400
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run( debug=True, host='0.0.0.0')
    # socketio.run(app, debug=True, async_mode='gevent')
