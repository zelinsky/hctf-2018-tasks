from flask import Flask, request, send_from_directory

app = Flask(__name__)

passwd = open("/opt/passwd.txt").read()
flag = open("/opt/flag.txt").read()


@app.route('/')
def index():
    userpw = request.args.get("passwd", "")
    if userpw == passwd:
        return flag, 200, {"Content-Type": "text/plain"}
    else:
        return '<html><body><form method="get"><input type="text" name="passwd" value="password"><input type="submit" value="login" /></form></body></html>'


if __name__ == '__main__':
    assert(len(passwd) == 3)
    assert(passwd.isdigit())
    app.run()
