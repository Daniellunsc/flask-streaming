# -*- Coding: utf-8 -*-

import datetime
from pydal import DAL, Field, exceptions, connection
import pymysql
import os


def model():
  print("chamando model")
  connection.ConnectionPool().close_all_instances(action='commit')
  try:
    dbinfo = os.environ['DBSTRING']
    db = DAL(dbinfo,  folder='./database', pool_size=0)
  except FileNotFoundError:
    os.mkdir('database')
  except pymysql.err.InternalError:
    db = DAL(dbinfo,  folder='./database', pool_size=0, migrate=True)
  finally:
    db.close()
    db = DAL(dbinfo,  folder='./database', pool_size=0, migrate=False)
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
