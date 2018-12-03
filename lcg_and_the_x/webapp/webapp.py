from flask import Flask, render_template, send_from_directory, request, session, redirect, url_for
from multiprocessing import Value
from PIL import Image
from lcg import LCG
import os


PIC_DIR = "static/pics"
TEMPL_PATH = "index.html"

current = len(os.listdir(PIC_DIR))

counter = Value('i', current)
app = Flask(__name__)
app.secret_key = b"tdAJDKAJSPIDU45SDA%&/()$"


def create_image_pw(path, user_id):
    l = LCG(user_id)
    buf = b""

    for _ in range(128):
        buf += l.next().to_bytes(16, "big")


    im = Image.frombytes("1", (128, 128), buf)
    im.save(os.path.join(path, "{}.bmp".format(user_id)))
    return l.next()


def do_signup():
    with counter.get_lock():
        counter.value += 1
        user_id = counter.value
    pw = create_image_pw(PIC_DIR, user_id)
    msg = """Congrats, you signed up!<br/>
    You can login with your user number and password:<br/>
    User Number: {} <br/>
    Password: {} <br/>
    Your personal password recovery token is:<br/>
    <img src="/static/pics/{}.bmp" /><br/>
    Make sure to keep this in a safe place!<br/>
    If you forget your password I can recover it for you if you provide this token!
    """.format(user_id, pw, user_id)
    return render_template(TEMPL_PATH, title="Success!", content=msg)


def do_login():
    user_id = int(request.form.get("user_id"))
    pw = int(request.form.get("pw"))

    lcg = LCG(user_id)
    for _ in range(128):
        lcg.next()
    if lcg.next() == pw:
        msg = "Login Successful<br/>"
        session['user_id'] = user_id
    else:
        msg = "Wrong credentials!"

    return render_template(TEMPL_PATH, title="Login!", content=msg)


def show_login_form():
    msg = """
    <h2 align="center"> Login:</h2>  
    <form method="POST">
    <table id="table1"; cellspacing="5px" cellpadding="5%"; align="center">  
       <tr>  
              <td  align="right" class="style1">User:</td>  
              <td class="style1"><input type="text" name="user_id" /></td>  
       </tr>   
       <tr>  
              <td align="right">Password:</td>  
              <td><input type="text" name="pw" /></td>  
       </tr>        
        <tr>  
        <td> <input type="submit" value="Submit" align="right"/>  
        <td>      
        </td>  
        </tr>  
</table>   
</form>
"""
    return render_template(TEMPL_PATH, title="Login!", content=msg) 

def show_signup_form():
    msg = """
    <h2 align="center"> SignUp:</h2>  
    <form method="POST" action="/signup">
    <table id="table1"; cellspacing="5px" cellpadding="5%"; align="center">  
       <tr>  
              <td  align="right" class="style1">Name:</td>  
              <td class="style1"><input type="text" name="Job Title" /></td>  
       </tr>   
       <tr>  
              <td align="right">Address:</td>  
              <td><input type="text" name="Company Name" /></td>  
       </tr>  
       <tr>  
              <td align="right">Country:</td>  
              <td><input type="text" name="Contact number" /></td>  
       </tr>  
       <tr>  
              <td align="right">Phone:</td>  
              <td><input type="text" name="Contact person" /></td>  
       </tr>        
        <tr>  
        <td> <input type="submit" value="Submit" align="right"/>  
        <td>      
        </td>  
        </tr>  
</table>   
</form>
"""
    return render_template(TEMPL_PATH, title="Sign up!", content=msg) 


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        return do_signup()
    else:
        return show_signup_form()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_login()
    else:
        return show_login_form()

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['user_id'] = None
    return redirect(url_for('home'))


@app.route('/')
def home():
    msg = """
    Hello! <br />
    This is the website for our on-campus fanclub of the band LCG and the X!<br />
    Everyone can signup for the club to: <br />
    <ul>
        <li>Get the latest LCG news</li>
        <li>Communicate with other fans</li>
        <li>Save secret messages prefixed with "flag{" (which is always handy...)</li>
    </ul>
    """
    return render_template(TEMPL_PATH, title="Home", content=msg)


@app.route('/flags')
def flag():
    if not session.get('user_id', None):
        return redirect(url_for('login'))
    if session['user_id'] != 1:
        msg = "The Flag storage is currently disabled, only flags that you already sumbitted will be shown here."
    else:
        msg = "flag{https://www.youtube.com/watch?v=NvS351QKFV4#Y0L0SW4G}"
    return render_template(TEMPL_PATH, title="Flag Storage", content=msg)


@app.route('/news')
def news():
    if not session.get('user_id', None):
        return redirect(url_for('login'))
    msg = """
    <h3>Website Launch</h3>
    I just took the website online. I wrote it myself! <br/>
    I also just signed up to make sure the signup process works.<br/>
    Then I created a secret flag, which worked as well!
    <hr>
    <h3>Flag Storage Maintenance</h3>
    Because of the new data protection laws in europe I decided to temporarily disable
    the secret flag storage... I hope i can bring it back up soon...
    """
    return render_template(TEMPL_PATH, title="News", content=msg)


@app.route('/static/<path:p>')
def wtf(p):
    return send_from_directory("static", p)

