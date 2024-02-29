from flask import Flask, render_template, redirect, url_for, request
from werkzeug.utils import secure_filename
import os

from model import ClassifierModel, device, class_names, transform
from engine import PredictOnImage

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

            gender = PredictOnImage(model=ClassifierModel,
                                    image_path='static/uploads/' + filename,
                                    class_names = class_names,
                                    transform=transform,
                                    device=device)

            return render_template('index.html', filename=filename, gender=gender)
        else:
            return 'Not allowed file.'

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/delete/<filename>', methods=['GET', 'POST'])
def delete_image(filename):
    os.remove(os.path.join(UPLOAD_FOLDER, filename))
    return redirect(url_for('home_page'), code=302)


if __name__ == '__main__':
    app.run(debug=True)