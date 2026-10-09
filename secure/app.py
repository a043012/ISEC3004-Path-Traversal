from flask import Flask, request, render_template
import os

app = Flask(__name__)

#Canonical absolute path of the only directory users are allowed to read from
REPORTS_DIR = os.path.realpath("reports")


@app.route("/")
def index():
    #User-controlled input from the URL, e.g. ?file=report.txt
    filename = request.args.get("file", "report.txt")
    #Build the candidate path under the trusted directory
    candidate = os.path.join(REPORTS_DIR, filename)
    #Canonicalise. Resolve "..", "." and symlinks into one absolute path
    canonical_candidate = os.path.realpath(candidate)
    #Block request if resolved path is outside REPORTS_DIR
    blocked = not (
        canonical_candidate == REPORTS_DIR
        or canonical_candidate.startswith(REPORTS_DIR + os.sep)
    )

    content = None
    error = None

    if blocked:
        error = "403 Forbidden - path traversal attempt detected and blocked."
        #Log attempt so it can be detected + traced
        print(f'[BLOCKED] requested_file="{filename}" resolved_path="{canonical_candidate}"')
    elif os.path.isfile(canonical_candidate):
        with open(canonical_candidate, "r") as file:
            content = file.read()
        print(f'[ALLOWED] requested_file="{filename}" resolved_path="{canonical_candidate}"')
    else:
        error = "File not found."

    #Return real HTTP status so blocked requests are not logged as 200
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
