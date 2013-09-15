#encoding=utf-8
import db_utils
from db_utils import db, to_dict
import models.user as user
import time

db.friend_request.save({'auto_incr_id' : 0})
def gen_request_id():
    id = db.friend_request.find_and_modify(update = {'$inc' : {'auto_incr_id' : 1}}, new = True).get('auto_incr_id')
    return id

class FriendRequestStatus:
    STATUS_INIT   = 0
    STATUS_ACCEPT = 1
    STATUS_DENY   = 2 

def make_request(from_uid, to_uid, message):
    if db.friend_request.find_one({'from_uid': from_uid, 'to_uid': to_uid, 'status': STATUS_INIT}) != None:
        return False, "request already exist"
    ts = time.time()
    id = gen_request_id()
    db.friend_request.insert({'request_id' : id,
                              'from_uid' : from_uid,
                              'to_uid' : to_uid,
                              'ts': ts,
                              'message': message,
                              'status': FriendRequestStatus.STATUS_INIT})
    return True, ''

def get_request(uid, status = -1):
    reqs = []
    if status == -1:
        reqs = db.friend_request.find({'to_uid': uid})
    else:
        reqs = db.friend_request.find({'to_uid': uid, 'status': status})
    return [to_dict(o) for o in reqs]

def change_request_status(request_id, status):
    r = db.friend_request.find_one({'request_id': request_id})
    if r != None:
        from_uid = r['from_uid']
        to_uid = r['to_uid']
        db.friend_request.update({'from_uid': from_uid, 'to_uid': to_uid}, {'$set': {'status': status}})
        if status == FriendRequestStatus.STATUS_ACCEPT:
            make_friend(to_uid, from_uid)

def make_friend(uid1, uid2):
    u1 = db.user.find_one({'uid': uid1})
    u2 = db.user.find_one({'uid': uid2})
    if u1 and u2:
        db.user.update({'uid': uid1}, {'$addToSet': {'friends': uid2}})
        db.user.update({'uid': uid2}, {'$addToSet': {'friends': uid1}})

def get_friend_list(uid):
    info = user.get_user_info(uid, ['friends'])
    if 'friends' in info.keys():
        return info['friends']
    return []

