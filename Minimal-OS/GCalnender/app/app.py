from flask import Flask, request, redirect, url_for, send_from_directory, render_template
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = '/app/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Scan the file using ClamAV
def scan_file(filepath):
    result = subprocess.run(['clamscan', filepath], stdout=subprocess.PIPE)
    return "OK" in result.stdout.decode()

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Scan the file for viruses
            if scan_file(filepath):
                return f'File {file.filename} uploaded and passed virus scan!'
            else:
                os.remove(filepath)
                return 'File failed virus scan and was deleted.'

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    <br>
    <a href="/files">View and Download Files</a>
    '''

@app.route('/files', methods=['GET', 'POST'])
def list_files():
    search_query = ""
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    
    if request.method == 'POST':
        search_query = request.form.get('search', '').lower()
        files = [f for f in files if search_query in f.lower()]

    return render_template('files.html', files=files, search_query=search_query)

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
