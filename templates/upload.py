import os
import json
import flask
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, make_response
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['pdf'])

app = Flask(__name__, path='')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


#import from all the other files
crimes_info = []
crimes = []
# rapsheet = 


''' 
Outputs a tuple of the rapsheet and results
    i.e.
        def __init__(self, crime_type, result, convict_date, offense, offense_code, prob_status):

        rapsheet = rs.Rapsheet(
            [
                rs.Crime("Misdemeanor", "Up To A Year In County Jail", two_years_ago, None, None, None),
                rs.Crime("Infraction", "Fine", week_ago, None, None, None)
            ])
        (i.e. the first element is the messages, the second is the result)
        results = [
            [[], "Discretionary"],
            [[], "Not Eligible"]
        ]

    would return (rapsheet, results)
'''
@app.route('/download/rapsheet')
def getOutputFromRapsheet(rapsheet):

    #vision = GOOGLEVISION(rapsheet)
    #     

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template("index.html", link="/upload")

# @app.route('/')
# @app.route('/index')
# def index():
#     user = {'username': 'Miguel'}
#     return render_template('index.html', title='Home', user=user)

@app.route('/review', methods=['GET', 'POST'])
def review():
    return render_template("step2.html", data=crimes_info, back="/upload", next="/download")


''' 
Given an input (rapsheer, results), 
will give an output of the format

    crimes = [
        {crime_type, result, convict_date, offsense, offense_code, prob_status, expunge_result, expunge_messages}
        {crime_type, result, convict_date, offsense, offense_code, prob_status, expunge_result, expunge_messages}
        {crime_type, result, convict_date, offsense, offense_code, prob_status, expunge_result, expunge_messages}
    ]
'''
@app.route('/download')
def formatOutput(input):
    return render_template("step3.html", data=crimes, back="/review", next="/download")


'''
Given an formatted input [input], 
will create an excel sheet
from this at the path [path] with the name [filename]

On success, returns the file path. On failure, 
returns None. 
'''
# def createExcelSheet(input, filename, path):
#     pass

def download_excel():
return send_from_directory(instance_path, path, mimetype=None, as_attachment=False, attachment_filename=None)

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
    return render_template("upload.html", back="/", next="/review")
    # '''
    # <!doctype html>
    # <title>Upload new File</title>
    # <h1>Upload new File</h1>
    # <form method=post enctype=multipart/form-data>
    #   <input type=file name=file>
    #   <input type=submit value=Upload>
    # </form>
    # '''





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
	app.run()