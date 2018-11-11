# -*- Coding: utf-8 -*-

"""
Module for auxiliary functions

"""

from flask import url_for
import glob

from mutagen import File
from model import model

MUSICFOLDER = 'static/musics/'

db = model()

def updateMusic():
    db._adapter.reconnect()
    musicList = glob.glob(MUSICFOLDER + '*.mp3')
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


def get_musics():
    musicList = db().select(db.musica.arquivo, db.musica.tempo, db.musica.cantor,
                            db.musica.nome, orderby=db.musica.arquivo | db.musica.nome)

    if len(musicList) > 0:
        musicJ = [{
            "fileName": mi.arquivo,
            "coverURL": url_for('coverImage', music=MUSICFOLDER + mi.arquivo),
            "fileUrl": url_for('sounds', music=MUSICFOLDER + mi.arquivo),
            "length": mi.tempo,
            "Tags": None
        } for mi in musicList]

        for i in range(len(musicJ)):
            if musicList[i].cantor is not None:
                musicJ[i]['Tags'] = {
                    'TIT2': musicList[i].nome,
                    'TPE1': musicList[i].cantor,
                }
    else:
        musicJ = []
    return musicJ


def sec2minString(sec):
    mi = sec / 60.0
    mi = str(mi).split(".")
    seci = int(float('0.' + mi[1]) * 60.0)
    if(seci < 10):
        seci = '0' + str(seci)
    else:
        seci = str(seci)

    return mi[0] + ":" + seci
