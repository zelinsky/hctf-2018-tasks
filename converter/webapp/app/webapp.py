from subprocess import Popen, PIPE, check_output, run

from flask import Flask, render_template, send_from_directory, request
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import json

from flask import redirect
from flask import url_for

app = Flask(__name__)
key = b'TB\xa7\x85\x80\xaf\xcc1\x896\xe6[J\xda\x05\xba'
cry_backend = default_backend()


whitelist_to = [
    "S5", "asciidoc", "beamer", "commonmark", "context", "docbook4", "docbook5", "dokuwiki", "dzslides", "dzslides",
    "gfm", "haddock", "html4", "html5", "icml", "json", "latex", "man", "ms", "markdown", "markdown_mmd",
    "markdown_phpextra", "markdown_strict", "mediawiki", "muse", "native", "opendocument", "opml", "org", "plain",
    "revealjs", "rst", "rtf", "slideous", "slidy", "texinfo", "textile", "zimwiki"
]


whitelist_from = [
    "commonmark", "creole", "docbook", "gfm", "haddock", "html", "latex", "markdown", "markdown_mmd",
    "markdown_phpextra", "markdown_strict", "mediawiki", "muse", "native", "opml", "org", "rst", "t2t",
    "textile", "tikiwiki", "twiki", "vimwiki"
]


def get_req_data():
    data = {
        "f": request.form.get("from"),
        "c": request.form.get("content"),
        "t": request.form.get("to")
    }
    return data


def encode_data(data):
    return json.dumps(data).encode(errors="ignore")


def decode_data(data):
    return json.loads(data.decode(errors="ignore"))


def pad(data):
    padder = padding.PKCS7(128).padder()
    return padder.update(data) + padder.finalize()


def unpad(data):
    padder = padding.PKCS7(128).unpadder()
    return padder.update(data) + padder.finalize()


def encrypt(data):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=cry_backend)
    encryptor = cipher.encryptor()
    ct = encryptor.update(pad(data))
    return iv + (ct + encryptor.finalize())


def decrypt(data):
    iv = data[:16]
    msg = data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=cry_backend)
    decryptor = cipher.decryptor()
    ct = unpad(decryptor.update(msg))
    return ct + decryptor.finalize()


def run_conversion(from_type, to_type, content):
    proc = run('pandoc --from {} --to {}'.format(from_type, to_type), shell=True, input=content.encode(), stdout=PIPE, timeout=2)
    if proc.returncode != 0:
        raise ValueError("Subproccess returned with exit code {}".format(proc.returncode))
    return proc.stdout.decode(errors="ignore")


@app.route('/')
def submit():
    return render_template("submit.html")


def do_create_cookie():
    data = get_req_data()

    # Make sure they're whitelisted
    if data["f"] not in whitelist_from or data["t"] not in whitelist_to:
        raise ValueError("Format not in whitelist")

    if len(data['c']) > 500:
        data['c'] = data['c'][:500]

    enc = encrypt(encode_data(data))

    resp = redirect(url_for("show"))
    resp.set_cookie("vals", enc.hex())

    return resp


def do_show():
    cookie = request.cookies.get("vals", "")
    if cookie:
        dec = decrypt(bytes.fromhex(cookie))
        data = decode_data(dec)
        return render_template("show.html", data=data)
    else:
        return redirect(url_for("submit"))


def do_func(f):
    try:
        return f()
    except Exception as ex:
        return "{}: {}".format(type(ex).__name__, str(ex))


@app.route("/show")
def show():
    return do_func(do_show)


@app.route("/create", methods=["POST"])
def create_cookie():
    return do_func(do_create_cookie)


def do_convert():
    cookie = request.cookies.get("vals", "")
    if cookie:
        data = decode_data(decrypt(bytes.fromhex(cookie)))
        conv = run_conversion(data['f'], data['t'], data['c'])
        return render_template("convert.html", data=conv)
    else:
        return redirect(url_for("submit"))


@app.route("/convert")
def convert():
    return do_func(do_convert)


@app.route('/static/<path:p>')
def wtf(p):
    return send_from_directory("static", p)


if __name__ == '__main__':
    app.run()
