from flask import Flask, url_for, render_template, json
from flask import send_file, request
import model
import glob

from io import BytesIO
from mutagen import File

app = Flask(__name__)

MUSICFOLDER = 'static/music'


def updateMusic():
    db = model()
    musicList = glob.glob(MUSICFOLDER + "*.mp3")
    musicNames = [mi.split("/")[-1] for mi in musicList]

    indb = [msi.arquivo for msi in db().iterselect(db.musica.arquivo)
            if msi.arquivo in musicNames]

    notindb = list(set(musicNames) - set(indb))
    for msi in notindb:
        tag = File(MUSICFOLDER + msi)
        tempo = sec2minString(tag.info.length)
        if 'TIT2' in tag.keys():
            db.musica.insert(nome=tag['TIT2'].text[0],
                             cantor=tag['TPE1'].text[0],
                             arquivo=msi,
                             tempo=tempo
                             )
        else:
            db.musica.insert(arquivo=msi, tempo=tempo)

    notindir = [msi.arquivo for msi in db().iterselect(
        db.musica.arquivo) if msi.arquivo not in musicNames]

    for msi in notindir:
        db(db.musica.arquivo == msi).delete()

    db.commit()


def sec2minString(sec):
    mi = sec / 60.0
    mi = str(mi).split(".")
    seci = int(float('0.' + mi[1]) * 60.0)
    if(seci < 10):
        seci = '0' + str(seci)
    else:
        seci = str(seci)

    return mi[0] + ":" + seci


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
    musiclist = glob.glob("static/musics/*.mp3")

    musicJ = [{"fileName": mi.split("/")[-1],
               "coverURL": url_for('coverImage', music=mi),
               'fileUrl':url_for('sounds', music=mi),
               'length': sec2minString(File(mi).info.length),
               'Tags': None
               } for mi in musiclist]

    for i in range(len(musicJ)):
        tag = File(musiclist[i])
        if('TIT2' in tag.keys()):
            musicJ[i]['Tags'] = {
                'TIT2': tag['TIT2'].text[0], 'TPE1': tag['TPE1'].text[0]}

    return render_template("home.html",
                           musicJ=musicJ)


if(__name__ == "__main__"):
    app.run(debug=True)
