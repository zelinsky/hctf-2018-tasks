from flask import Flask, render_template, session, request, url_for, redirect
from pyArango.connection import * 

# Flask
from pyArango.theExceptions import QueryError, ConnectionError, CreationError

app = Flask(__name__)
app.secret_key = 'qildEd3YU1C9bE7T/eFcCivT/DCAxsLf'

FLAG = open("flag.txt").read()

MSG = [
    "",
    "Success!",
    "The user's 'role' is not 'admin'!",
    "User/Password comination does not exist!"
]

def check_creds(user, passwd):
    conn = Connection(arangoURL="http://db:8529", username="dbuser@arango", password="ladskjqoi3242")
    user_db = conn['user_db']
    users = user_db.AQLQuery(
        "FOR u IN users FILTER u.user == '{}' && u.passwd == '{}' RETURN u".format(user, passwd)
    )
    if len(users):
        user = users[0]
        if user['role'] == "admin":
            return True, 1
        else:
            return False, 2
    else:
        return False, 3


@app.route('/')
def index():
    user = session.get('username', 'visitor')
    return render_template('index.html', user=user)


@app.route("/admin/", methods=["GET"])
@app.route("/admin/?msg_id=<int:msg_id>", methods=["GET"])
def login(msg_id=0):
    return render_template("login.html", msg=MSG[msg_id])


@app.route("/admin_login", methods=["POST"])
def do_login():
    user = request.form['user']
    passwd = request.form['passwd']
    try:
        res, msg_id = check_creds(user, passwd)
        if res:
            session['username'] = user
            return "Nothing here. Meanwhile: " + FLAG
        else:
            return redirect(url_for('login', msg_id=msg_id))
    except Exception as ex:
        return str(ex)


if __name__ == '__main__':
    app.run()
