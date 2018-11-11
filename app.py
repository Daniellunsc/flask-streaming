from flask import Flask, url_for, render_template, json
from flask import send_file, request
import model
import glob

from io import BytesIO
from mutagen import File

app = Flask(__name__)

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
