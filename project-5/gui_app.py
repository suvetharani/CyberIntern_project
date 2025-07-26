from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from encryption import generate_key_iv, encrypt_file, decrypt_file
import hashlib
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages

# Directories
UPLOAD_DIR = "uploads"
ENC_DIR = "encrypted"
DEC_DIR = "decrypted"
META_FILE = "metadata.json"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(ENC_DIR, exist_ok=True)
os.makedirs(DEC_DIR, exist_ok=True)

def hash_file(data):
    return hashlib.sha256(data).hexdigest()

@app.route('/')
def index():
    return render_template("index.html")
@app.route('/encrypt', methods=['POST'])
def encrypt_route():
    if 'file' not in request.files:
        flash("No file part")
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        flash("No selected file")
        return redirect(url_for('index'))

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_DIR, filename)
        file.save(filepath)

        with open(filepath, "rb") as f:
            data = f.read()

        # Encrypt
        key, iv = generate_key_iv()
        ciphertext = encrypt_file(data, key, iv)
        hash_val = hash_file(ciphertext)

        enc_filename = filename + ".enc"
        enc_path = os.path.join(ENC_DIR, enc_filename)
        key_path = enc_path + ".key"

        with open(enc_path, "wb") as f:
            f.write(ciphertext)

        with open(key_path, "wb") as f:
            f.write(key + iv)

        # Save metadata
        metadata = {
            "filename": enc_filename,
            "time": datetime.now().isoformat(),
            "hash": hash_val
        }
        with open(META_FILE, "w") as f:
            json.dump(metadata, f, indent=4)

        flash(f"✅ File encrypted! <a href='/download/{enc_filename}'>Download Encrypted File</a><br><a href='/download/{enc_filename}.key'>Download Key File</a>")
        return redirect(url_for('index'))

@app.route('/decrypt', methods=['POST'])
def decrypt_route():
    enc_file = request.files.get('enc_file')
    key_file = request.files.get('key_file')

    if not enc_file or not key_file:
        flash("Both encrypted file and key file are required.")
        return redirect(url_for('index'))

    # Save uploaded files
    enc_filename = secure_filename(enc_file.filename)
    key_filename = secure_filename(key_file.filename)

    enc_path = os.path.join(UPLOAD_DIR, enc_filename)
    key_path = os.path.join(UPLOAD_DIR, key_filename)

    enc_file.save(enc_path)
    key_file.save(key_path)

    try:
        with open(enc_path, "rb") as f:
            ciphertext = f.read()
        with open(key_path, "rb") as f:
            key_iv = f.read()

        key, iv = key_iv[:32], key_iv[32:]

        decrypted_data = decrypt_file(ciphertext, key, iv)

        # Load and verify metadata
        with open(META_FILE) as f:
            metadata = json.load(f)

        if hash_file(ciphertext) == metadata["hash"]:
            flash("✅ Hash verified. File is untampered.")
        else:
            flash("⚠️ File integrity check failed!")

        # Save decrypted file
        original_name = enc_filename.replace(".enc", "_decrypted")
        dec_path = os.path.join(DEC_DIR, original_name)

        with open(dec_path, "wb") as f:
            f.write(decrypted_data)

        flash(f"✅ File decrypted! <a href='/download/{original_name}'>Download Decrypted File</a>")
        return redirect(url_for('index'))

    except Exception as e:
        flash(f"Error during decryption: {str(e)}")
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    for folder in [ENC_DIR, DEC_DIR, UPLOAD_DIR]:
        file_path = os.path.join(folder, filename)
        if os.path.exists(file_path):
            return send_from_directory(folder, filename, as_attachment=True)
    flash("File not found!")
    return redirect(url_for('index'))

# More routes coming in next steps (encrypt, decrypt)

if __name__ == "__main__":
    app.run(debug=True)
