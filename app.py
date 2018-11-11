from flask import Flask, url_for, render_template
from flask import send_file, request, flash, redirect

import flask_login
from passlib.hash import sha256_crypt
from flask_mail import Mail
import datetime

from tools import *
from model import model
from os import urandom

app = Flask(__name__)
app.secret_key = urandom(24)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

app.config.update(
    DEBUG=True,
    # Email Settings
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_SSL=False,
    # Change email and password to send emails.
    MAIL_USERNAME='myemail@gmail.com',
    MAIL_PASSWORD='mypassword'
)

mail = Mail(app)


@app.route('/register', methods=['GET', 'POST'])
def register():
    db = model()
    if request.method == "POST":
        name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        query = db(db.user.email == email)
        if query.isempty() is True:
            password = sha256_crypt.encrypt(password)
            db.user.insert(name=name, email=email, password=password)
            db.commit()
            return redirect(url_for('login'))
        else:
            return render_template('register.html')
    else:
        return render_template('register.html')


@app.route("/sounds")
def sounds():
    music = request.args["music"]
    return send_file(music, mimetype="audio/mp3")


@app.route("/coverImage")
def coverImage():
    cover = request.args["music"]
    print(cover)
    cover = File(cover)
    print(cover.tags.keys())
    if("APIC:Front" in cover.tags.keys()):
        imgcover = cover.tags["APIC:Front"].data
        strIO = BytesIO()
        strIO.write(imgcover)
        strIO.seek(0)

        return send_file(strIO,
                         mimetype="image/jpg")
    else:
        return app.send_static_file('images/noCoverImage.png')


@app.after_request
def add_header(response):
    response.cache_control.max_age = 0
    return response


@app.route("/")
def home():
    updateMusic()
    musicJ = get_musics()
    return render_template("home.html",
                           musicJ=musicJ)


if(__name__ == "__main__"):
    app.run(debug=True)
