#ISEC3004 Path Traversal
Path Traversal vulnerability and security-enhanced code. 

1. Vunerability code
To execute the code, run:
    python3 -m pip install flask
    python3 app.py
    -> http://127.0.0.1:5000/?file=report.txt   (legitimate, works)
    -> http://127.0.0.1:5000/?file=../private/secret.txt   (Exploit)
