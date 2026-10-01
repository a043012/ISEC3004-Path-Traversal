from flask import Flask, request, render_template
import os
app = Flask(__name__)
@app.route("/")
def index():
    # Filename comes straight from the URL query string. ].
    filename = request.args.get("file", "report.txt")
    # The intention is to serve files from the "reports" directory, but ".." sequences or absolute paths let the user escape it.
    # Risk: path traversal, example: ?file=../app.py or ?file=/etc/passwd
    # can expose source code, credentials, and system files.
    file_path = os.path.join("reports", filename)
    content = None
    error = None
    if os.path.isfile(file_path):
        with open(file_path, "r") as file:
            content = file.read()
    else:
        error = "File not found."
    # Risk: Leaking server directory structure, showing visitors the server's internal folder layout, which helps attackers.
    return render_template("index.html", content=content, error=error, requested_path=file_path)
if __name__ == "__main__":
    # Risk:  if the site breaks, debug mode shows outsiders its inner workings.
    app.run(host="127.0.0.1", port=5000, debug=True)





