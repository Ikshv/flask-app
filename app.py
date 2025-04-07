from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import os
import time

app = Flask(__name__)

# Directory where the files will be uploaded
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowable file extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'dmg', 'exe'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    # Get the list of files in the upload folder
    files = os.listdir(UPLOAD_FOLDER)
    # Get metadata for each file
    file_metadata = []
    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file)
        file_size = os.path.getsize(file_path)
        last_modified = time.ctime(os.path.getmtime(file_path))  # Convert timestamp to readable format
        file_metadata.append({
            'filename': file,
            'size': file_size,
            'last_modified': last_modified
        })
    return render_template('index.html', files=file_metadata)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return redirect(url_for('index'))

    return 'File type not allowed', 400

@app.route('/download/<filename>')
def download(filename):
    # Send the file from the upload folder
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/delete/<filename>', methods=['POST'])
def delete(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)  # Delete the file
    return redirect(url_for('index'))

if __name__ == "__main__":
    # Ensure the uploads folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    app.run(debug=True, host="0.0.0.0", port=5010)
