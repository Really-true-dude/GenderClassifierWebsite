from flask import Flask, render_template, redirect, url_for, request
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route("/upload", methods=['POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part!'
        file = request.files['file']
        if file.filename == '':
            return 'No file selected!'
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join( UPLOAD_FOLDER, filename))

            return render_template('index.html', filename=filename)
        else:
            return 'Not allowed file.'

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', 'uploads/' + filename), code=301)

if __name__ == '__main__':
    app.run(debug=True)