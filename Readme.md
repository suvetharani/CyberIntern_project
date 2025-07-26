# 🔐 Cybersecurity Toolkit: Password Analyzer & AES File Encryptor

A dual-featured web application combining two practical cybersecurity tools:
- **Password Strength Analyzer** with custom wordlist generation
- **AES-256 File Encryptor Web App** for secure file handling

---

## 1️⃣ Password Strength Analyzer

### 📌 Features
- Strength analysis using `zxcvbn`
- Time-to-crack estimates & suggestions
- Custom wordlist generation from:
  - Name, pet name, birth year, custom keywords
  - Variations like leetspeak, reversed, years
- Downloadable wordlist as `.txt`
- Web UI built with Flask + HTML/CSS

### 🛠️ Tech Stack
Python · Flask · zxcvbn · NLTK · HTML/CSS

### 🚀 Run
```bash
pip install flask zxcvbn nltk
python gui_app.py
```

# Visit http://localhost:5000

---

2️⃣ AES File Encryptor Web App
🔐 Features
AES-256 file encryption & decryption

SHA-256 integrity check

Web interface for file uploads/downloads

Key + IV auto-generated and saved

Metadata logging with timestamp & hash

🛠️ Tech Stack
Python · Flask · cryptography · SHA-256 · Bootstrap

🚀 Run
```
pip install flask cryptography
python app.py
```

# Visit http://localhost:5000

🧪 Process
Upload ➝ Encrypt ➝ Get .enc & .key

Upload both ➝ Decrypt ➝ Verify hash ➝ Download
