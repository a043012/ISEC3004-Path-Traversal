"""
app.py - SECURE VERSION (mitigated)

ISEC3004 Assignment 1 - Path Traversal (CWE-22) MITIGATION

Security-enhanced counterpart of the vulnerable app.py. Same route, same
template, but the file path is now canonicalized and validated before
being opened.

Mitigation technique: "Canonicalize path names before validating them"
(same principle as Lab 7's IDS02-J guidance):
    1. os.path.realpath() resolves the requested path to its canonical,
       absolute form (collapsing "..", ".", and symlinks).
    2. The canonical path is compared against the canonical, trusted
       "reports" directory. If the requested file is NOT inside it, the
       request is rejected and logged as a blocked attempt - this is NOT
       just a string check for ".." (which can be bypassed by encoding);
       canonicalizing first makes the check robust.

Run:
    python3 -m pip install flask
    python3 app.py
    -> http://127.0.0.1:5000/?file=report.txt              (still works)
    -> http://127.0.0.1:5000/?file=../private/secret.txt   (now BLOCKED)
"""

from flask import Flask, request, render_template
import os

app = Flask(__name__)

REPORTS_DIR = os.path.realpath("reports")


@app.route("/")
def index():
    filename = request.args.get("file", "report.txt")

    # --- MITIGATION ----------------------------------------------------------
    # Step 1: build the candidate path under the trusted directory.
    candidate = os.path.join(REPORTS_DIR, filename)

    # Step 2: canonicalize - resolves any ".." / "." / symlinks into a
    # single, unambiguous absolute path.
    canonical_candidate = os.path.realpath(candidate)

    # Step 3: containment check - the canonical path MUST still be inside
    # REPORTS_DIR. If not, this is a path traversal attempt -> block it.
    blocked = not (
        canonical_candidate == REPORTS_DIR
        or canonical_candidate.startswith(REPORTS_DIR + os.sep)
    )
    # ---------------------------------------------------------------------------

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
