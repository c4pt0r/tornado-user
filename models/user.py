#encoding=utf-8
import db_utils
from db_utils import db, to_dict

class UserErrorCode:
    ERR_OK               =  0
    ERR_INVALID_FORM     = -1
    ERR_NO_SUCH_USER     = -2
    ERR_EMAIL_DUPLICATED = -3
    ERR_PASSWORD_ERROR   = -4

db.user.save({'auto_incr_id' : 0})

def gen_user_id():
    id = db.user.find_and_modify(update = {'$inc' : {'auto_incr_id' : 1}}, new = True).get('auto_incr_id')
    return id

# return value:  error_code, msg
# 0 means OK
def register_user(**kw):
    if 'email' not in kw.keys() and 'password' not in kw.keys():
        return UserErrorCode.ERR_FORM_INVALID, "form invalid"

    if db.user.find_one({'email': kw['email']}) != None:
        return UserErrorCode.ERR_EMAIL_DUPLICATED, "email exists"

    kw['uid'] = gen_user_id()
    db.user.insert(kw)

    return UserErrorCode.ERR_OK, ""

def auth(email, password):
    if db.user.find_one({'email': email, 'password': password}) == None:
        return UserErrorCode.ERR_PASSWORD_ERROR, "email or password error"
    return UserErrorCode.ERR_OK, ""

#get user info,   fields is a list -> ['uid', 'email', ...]  or [] means all field
def get_user_info(email_or_uid, fields = None):
    email = None
    uid = None
    if type(email_or_uid) == str:
        email = email_or_uid
    elif type(email_or_uid) == int:
        uid = email_or_uid
    u = None
    if fields == None or len(fields) == 0:
        fields = None
    else:
        fields = {}.fromkeys(fields, 1)
    if email != None:
        print email
        u = db.user.find_one({'email': email}, fields)
    if uid != None:
        u = db.user.find_one({'uid': uid}, fields)
    return to_dict(u)
