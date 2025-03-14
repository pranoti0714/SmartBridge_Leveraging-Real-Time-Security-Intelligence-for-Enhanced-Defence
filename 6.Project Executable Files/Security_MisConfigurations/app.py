from flask import Flask, render_template, send_from_directory, abort
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ✅ Disable Debug Mode (Security Fix)
app.config['DEBUG'] = False

# ✅ Secure Secret Key (Environment Variable)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "default_secret_key")

# ✅ Secure Uploads Folder
UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('index.html')

# ✅ Prevent Directory Listing
@app.route('/uploads/')
def list_files():
    abort(403)  # Block file listing

# ✅ Secure File Downloads
@app.route('/uploads/<path:filename>')
def download_file(filename):
    safe_filename = secure_filename(filename)  # Prevent directory traversal
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)

    if not os.path.exists(file_path):  
        abort(404)  # Return 404 if file doesn't exist

    return send_from_directory(app.config['UPLOAD_FOLDER'], safe_filename)

if __name__ == '__main__':
    app.run()
