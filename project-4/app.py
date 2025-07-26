from flask import Flask, render_template, request, send_file
from analyzer import analyze_password
from wordlist_generator import generate_wordlist, export_wordlist
from utils import clean_input

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    wordlist_ready = False

    if request.method == "POST":
        password = request.form.get("password")
        inputs = [
            clean_input(request.form.get("name")),
            clean_input(request.form.get("pet")),
            clean_input(request.form.get("dob")),
            *request.form.get("custom", "").split()
        ]

        # Analyze password
        result = analyze_password(password)

        # Generate and export wordlist
        wordlist = generate_wordlist(inputs)
        export_wordlist(wordlist)
        wordlist_ready = True

    return render_template("index.html", result=result, wordlist_ready=wordlist_ready)

@app.route("/download")
def download():
    return send_file("wordlist.txt", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
