import os
from flask import Flask, render_template, jsonify, request
from werkzeug.utils import secure_filename

templateDirectory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app/backend/templates')
staticDirectory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app/backend/static')


UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = set(['eml'])

app = Flask(
    __name__,
    template_folder = templateDirectory,
    static_folder = staticDirectory
)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



@app.route('/')
def index():
    return render_template('index.html')\

@app.route('/')
def upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html')


if __name__ == "__main__":
    app.run()