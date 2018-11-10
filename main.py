from flask import Flask, url_for, render_template
from flask import request, send_file
import json
import glob

app = Flask(__name__)

@app.route("/")
def home():
   musicList = glob.glob("static/musics/*.mp3")

   musicJ = [{'filename': mi.split("/")[-1],
              'fileURL': url_for('sounds', music=mi)} for mi in musicList]
   return render_template("home.html", musicJ=musicJ)


@app.route("/sounds")
def sounds():
  music = request.args["music"]
  return send_file(music, mimetype="audio/mp3")

if(__name__ == "__main__"):
    app.run()