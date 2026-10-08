from flask import Flask, request, render_template
import os

app = Flask(__name__)

REPORTS_DIR = os.path.realpath("reports")


@app.route("/")
def index():
    filename = request.args.get("file", "report.txt")
    candidate = os.path.join(REPORTS_DIR, filename)
    canonical_candidate = os.path.realpath(candidate)
    blocked = not (
        canonical_candidate == REPORTS_DIR
        or canonical_candidate.startswith(REPORTS_DIR + os.sep)
    )

    content = None
    error = None

    if blocked:
        error = "403 Forbidden - path traversal attempt detected and blocked."
        print(f'[BLOCKED] requested_file="{filename}" resolved_path="{canonical_candidate}"')
    elif os.path.isfile(canonical_candidate):
        with open(canonical_candidate, "r") as file:
            content = file.read()
        print(f'[ALLOWED] requested_file="{filename}" resolved_path="{canonical_candidate}"')
    else:
        error = "File not found."

    status_code = 403 if blocked else 404 if error else 200

    return render_template(
        "index.html",
        content=content,
        error=error,
        requested_path=canonical_candidate,
        blocked=blocked,
    ), status_code


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
