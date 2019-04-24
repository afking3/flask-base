import os
import json
import flask
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, make_response
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['pdf'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

crimes = [
    {
        "id": 1,
        "expungement": "felony",
        "name": "Tom",
        "location": "Los Angeles",
        "date": "2018-01-01"
    },
    {
        "id": 2,
        "expungement": "felony",
        "name": "Jerry",
        "location": "Los Angeles",
        "date": "2018-02-02"
    },
    {
        "id": 3,
        "expungement": "infraction",
        "name": "Spike",
        "location": "Los Angeles",
        "date": "2018-03-03"
    }
]


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return  render_template("index.html", link="/upload")


@app.route('/<page>')
def next(page):
    return  render_template(page)

# @app.route('/')
# @app.route('/index')
# def index():
#     user = {'username': 'Miguel'}
#     return render_template('index.html', title='Home', user=user)

@app.route('/review', methods=['GET', 'POST'])
def review():
    return render_template("step2.html", data=crimes, back="/upload", next="/download")

@app.route('/download')
def download():
    return render_template("step3.html", data=crimes, back="/review", next="/download")

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('show',
                                    filename=filename))
    return render_template('upload.html', back="/", next="/review")




# @app.route('/uploads/<id>')
# def get_pdf(id=None):
#     if id is not None:
#         binary_pdf = get_binary_pdf_data_from_database(id=id)
#         response = make_response(binary_pdf)
#         response.headers['Content-Type'] = 'application/pdf'
#         response.headers['Content-Disposition'] = \
#             'inline; filename=%s.pdf' % id
#         return response

# @app.route('/<id>')
# def show_pdf(id=None):
#     if id is not None:
#         return render_template('doc.html', doc_id=id)
@app.route('/show/<filename>', methods=['GET', 'POST'])
def show(filename):
#     filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#     print(os.listdir(app.config['UPLOAD_FOLDER']))
    # filepath = app.config['UPLOAD_FOLDER'] + "/"+ filename
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('show',
                                    filename=filename))

    return render_template('step1.html', reupload="/upload", back="/", next="/review", filename=filename)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    print(filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
# @app.route('/show/<filename>')
# def uploaded_file(filename):
#     print()
#     filename = UPLOAD_FOLDER + filename
#     return render_template('step1.html', filename=filename)

if __name__== "__main__":
	# db.create_all() #do only once
    app.secret_key = b'486995feb1ce1b4d2e282a6b31cb3bfbd90ef8ce33713783'    
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()

