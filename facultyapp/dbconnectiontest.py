
from flask import Flask, request
from flask_api_builder import make_api
from flask_api_builder import APIGenerator
# from flask_restframework import
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify
from flask.json import jsonify
import os
import sys
#import xlrd
import pymysql
import pymysql.connections
#import pandas as pd
#from pandas.io import sql
import csv
#import SqlExecutor
import SqlExecutor
#from src
#import url1
from sqlalchemy import create_engine
#from urllib3 import poolmanager
import sqlalchemy
from sqlalchemy import exc
import Logger
import MbConfig
from sqlalchemy import text
from MySQLdb import connect
from sqlalchemy import create_engine

obj=APIGenerator()
data1=obj.preamble();
app = data1("__main__")
api = data1(app)
print(api)

driver = 'mysql'
host = 'localhost'
name = 'test_django'
username = 'root'
password = ''
def connectEngine(engine):
    try:
        cnxn = engine.connect()
        return cnxn
    except (sqlalchemy.exc.InterfaceError, e):
        Logger.error(e)
        raise
sqlEx = SqlExecutor.SqlExecutor()
conn = sqlEx.getConnectionString(driver, host, name, username, password)
conn="mysql+pymysql://root:"+''+"@localhost/test_django"
engine = create_engine(conn, pool_size=20, max_overflow=0)
cnxn = connectEngine(engine)
# cnxn.query("select * from testapp")
class Data:
    def get(self):
        query = cnxn.execute("select * from testapp")  # This line performs query and returns json result
        res={'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        print(res)
        json=dumps(res)
        print (json)
api.add_resource(Data, '/data')

