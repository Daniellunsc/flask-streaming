from flask import Flask, url_for, render_template
from flask import request, send_file
import json
import glob
from mutagen import File
from io import BytesIO

app = Flask(__name__)

@app.route("/")
def home():
  musicList = glob.glob("static/musics/*.mp3")

  musicJ = [{'filename': mi.split("/")[-1],
            'fileURL': url_for('sounds', music=mi)} for mi in musicList]
  
  for i in range(len(musicJ)):
    tag = File(musicList[i])
    if('TIT2' in tag.keys()):
      musicJ[i]['Tags'] = {'TIT2': tag['TIT2'].text[0], 'TPE1': tag['TPE1'].text(0)}
  
  return render_template("home.html", musicJ=musicJ)


@app.route("/sounds")
def sounds():

  music = request.args["music"]
  return send_file(music, mimetype="audio/mp3")

@app.route("/coverimage")
def coverimage():
  cover = request.args["music"]
  cover = File(cover)
  if("APIC:" in cover.tags.keys()):
    imgcover = cover.tags["APIC:"].data
    strIO = BytesIO()
    strIO.write(imgcover)
    strIO.seek(0)

    return send_file(strIO, mimetype="image/jpg")
  else:
    return app.send_static_file('images/noCoverImage.png')


def sec2min(sec):
  minutes = sec / 60.0
  minutes = str(minutes).split(".")
  seci = int(float('0.' + minutes[1]) * 60.0)
  if(seci < 10):
    seci = '0' + str(seci)
  else:
    seci = str(seci)
  return minutes[0] + ":" + seci

if(__name__ == "__main__"):
    app.run()