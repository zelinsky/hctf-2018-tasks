from flask import Flask, request, send_from_directory

app = Flask(__name__)

names = [
    "theseus",
    "jobs",
    "wiesner",
    "bezos",
    "gates",
    "stallman",
    "selfridge",
    "hal9000",
    "schwalm"
]

BODY = """
<html><head><title>Know Your History</title></head>
<body>
<div style="margin: 0 auto">
<h1>Name Game</h1>
Name at least 8 out of the 9 protagonists from the following scenes (only family names for actual people) to get the flag.


<form method="post">
{}
<input type="submit" value="Submit" />
</form>
</div>
</body>
</html>
"""

row_template = "<div><img src='img/{num}.png' width='200px' /><input type='text' name='{num}' value='{guess}' />{msg}</div>"


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        guesses = []
        for i in range(len(names)):
            guesses.append(request.form.get(str(i), ""))
        return build_page(names, BODY, guesses)
    else:
        return build_page(names, BODY)


def build_page(names, body, guesses=[]):
    inner = ""
    has_guessed = False

    if len(guesses) == len(names):
        has_guessed = True

    correct = 0
    for i in range(len(names)):
        msg = ""
        if has_guessed:
            if guesses[i].lower() == names[i]:
                msg = "Correct"
                correct += 1
            elif guesses[i]:
                msg = "Incorrect"

        inner += row_template.format(num=i, msg=msg, guess=guesses[i] if len(guesses) > i else "")

    if correct >= 8:
        return "Congrats: " + open("/opt/flag.txt").read()

    return body.format(inner)


@app.route('/img/<path:path>')
def send_js(path):
    return send_from_directory('img', path)


if __name__ == '__main__':
    BODY = build_page(names, BODY)
    app.run()
