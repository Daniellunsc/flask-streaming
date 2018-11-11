# -*- Coding: utf-8 -*-

import datetime
from pydal import DAL, Field
import os


def model():
    dbinfo = os.environ['DBSTRING']
    if not os.path.exists('/database'):
      os.mkdir('database')
    db = DAL(dbinfo,  folder='./database', pool_size=1)
    table(db)
    return db


def table(db):

    db.define_table("user",
                    Field("name", "string"),
                    Field("email", "string"),
                    Field("password", "password"))

    db.define_table("genero", Field("nome", "string"))

    db.define_table("musica",
                    Field("nome", "string"),
                    Field("cantor", "string"),
                    Field("album", "string"),
                    Field("arquivo", "string"),
                    Field("tempo", "string"),
                    Field("genero", "list:reference genero"),
                    )

    db.define_table("preferidas",
                    Field("musica", "reference musica"),
                    Field("user", "reference user"),
                    )

    db.define_table("tocada",
                    Field("tocadaem", "datetime",
                          default=datetime.datetime.now()),
                    Field("musica", "reference musica"),
                    Field("user", "reference user")
                    )
