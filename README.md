#ISEC3004 Path Traversal
Path Traversal vulnerability and security-enhanced code. 

1. Vunerability code
To execute the code, run:
    python3 -m pip install flask
    sudo python3 app.py (the reason to use sudo is that I have already set up the permission)
    -> http://127.0.0.1:5000/?file=report.txt   (legitimate, works)
    -> http://127.0.0.1:5000/?file=../private/secret.txt   (Exploit)

2. Security code
To handle the problem , I implement the line code os.path.realpath() before using it 
Returns clear status codes: 200 success, 403 blocked attack, 404 file not found
