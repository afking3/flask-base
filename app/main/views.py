from flask import Blueprint, render_template
import os
import json
import flask
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, make_response, send_file
from werkzeug.utils import secure_filename
from app.main import main2
from app.models import EditableHTML


main = Blueprint('main', __name__)



UPLOAD_FOLDER = 'app/main/uploads'
ALLOWED_EXTENSIONS = set(['pdf'])

@main.route('/about')
def about():
    editable_html_obj = EditableHTML.get_editable_html('about')
    return render_template(
        'main/about.html', editable_html_obj=editable_html_obj)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
def index():
    print("accessed")
    return  render_template("index.html", link="/upload/")


@main.route('/<page>')
def next(page):
    return  render_template(page)

@main.route('/download/<filename>')
def download(filename):
    # x = main2.getTestInput()
    x = main2.getOutputFromRapsheet(filename)
    output = main2.formatOutput(x)
    print(output)
    excel = main2.createExcelSheet(output, "output.xls", "app/main/output/")
    return render_template("step3.html", data=output, back=url_for('main.show', filename=filename), next=url_for('main.download', filename=filename))

@main.route('/return-files/')
def download_excel():
    return send_file('app/main/output/output.xls',
                     attachment_filename='output.xls',
                     as_attachment=True)

@main.route('/upload/', methods=['GET', 'POST'])
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
            print(filename)
            file.save(os.path.join("app/main/uploads", filename))
            return redirect(url_for('main.show',
                                    filename=filename))
    return render_template('upload.html', back="/")



@main.route('/show/<filename>', methods=['GET', 'POST'])
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
            file.save(os.path.join("app/main/uploads/", filename))
            return redirect(url_for('main.show',
                                    filename=filename))

    return render_template('step1.html', reupload="/upload/", back="/", next = url_for('main.download', filename=filename), filename=filename)


@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join("/", 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

@main.route('/uploads/<filename>')
def uploaded_file(filename):
    print("***********")
    print(filename)
    print("***********")
    print(os.listdir("app/main/uploads/"))
    return send_from_directory("app/main/uploads/", filename, as_attachment=True)
# @main.route('/show/<filename>')
# def uploaded_file(filename):
#     print()
#     filename = UPLOAD_FOLDER + filename
#     return render_template('step1.html', filename=filename)
