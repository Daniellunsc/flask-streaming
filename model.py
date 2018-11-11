# -*- Coding: utf-8 -*-

import datetime
from pydal import DAL, Field, exceptions, connection
import pymysql
import os


def model():
  try:
    dbinfo = os.environ['DBSTRING']
    if connection.ConnectionPool().check_active_connection:
      print("conexao existente, usando ela")
      db = connection.ConnectionPool().reconnect()
      return db
    else:
      print("conexao nao existente, usando outra")
      connection.ConnectionPool().close_all_instances(action='commit')
      db = DAL(dbinfo,  folder='./database', pool_size=1)
  except FileNotFoundError:
    os.mkdir('database')
  except pymysql.err.InternalError:
    connection.ConnectionPool().close_all_instances(action='commit')
    db = DAL(dbinfo,  folder='./database', pool_size=1, migrate=True)
  finally:
    connection.ConnectionPool().close_all_instances(action='commit')
    db = DAL(dbinfo,  folder='./database', pool_size=1, migrate=False)
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
