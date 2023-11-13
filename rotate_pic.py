from flask import Flask, render_template, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('rotate_index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file1 = request.files['file1']
        file2 = request.files['file2']
        filenames = []
        for file in [file1, file2]:
            if file:
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)
                filenames.append(file.filename)
        return render_template('rotate_index.html', filenames=filenames)

if __name__ == '__main__':
    app.run(debug=True)
