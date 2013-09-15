#encoding=utf-8
import pymongo

db_info_test = {
    'host' : 'localhost',
    'port' : 27017,
    'db'   : 'test',
}

con = None
db = None

def init_db(profile):
    global con, db
    con = pymongo.Connection(profile['host'], profile['port'])
    db = con[profile['db']]

def to_dict(o):
    del o['_id']
    return o
