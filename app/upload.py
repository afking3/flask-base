import os
import json
import flask
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, make_response, send_file
from werkzeug.utils import secure_filename
from __init__.py import create_app
import main2

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['pdf'])

app = create_app("production")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return  render_template("index.html", link="/upload/")


@app.route('/<page>')
def next(page):
    return  render_template(page)

@app.route('/download/<filename>')
def download(filename):
    # x = main2.getTestInput()
    x = main2.getOutputFromRapsheet(filename)
    output = main2.formatOutput(x)
    print(output)
    excel = main2.createExcelSheet(output, "output.xls", "output/")
    return render_template("step3.html", data=output, back=url_for('show', filename=filename), next=url_for('download', filename=filename))

@app.route('/return-files/')
def download_excel():
    return send_file('output/output.xls',
                     attachment_filename='output.xls',
                     as_attachment=True)

@app.route('/upload/', methods=['GET', 'POST'])
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
    return render_template('upload.html', back="/")



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

    return render_template('step1.html', reupload="/upload/", back="/", next = url_for('download', filename=filename), filename=filename)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

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
    app.run(debug=False)
