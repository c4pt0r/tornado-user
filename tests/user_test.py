import db_utils
db_utils.init_db(db_utils.db_info_test)

import unittest
import models.user as user

class TestUserFunctions(unittest.TestCase):
    def setUp(self):
        pass

    def test_init(self):
        code, msg = user.register_user(email="c4pt0r@126.com", password="shit")
        self.assertEqual(code, user.UserErrorCode.ERR_OK)
        code, msg = user.register_user(email="c4pt0r@126.com", password="shit")
        self.assertEqual(code, user.UserErrorCode.ERR_EMAIL_DUPLICATED)

        info = user.get_user_info("c4pt0r@126.com", [])
        self.assertEqual(code, user.UserErrorCode.ERR_EMAIL_DUPLICATED)
        self.assertEqual(info['uid'], 1)

        code, msg = user.auth("c4pt0r@126.com", "shit")
        self.assertEqual(code, user.UserErrorCode.ERR_OK)

        code, msg = user.auth("c4pt0r@126.com", "shit2")
        self.assertEqual(code, user.UserErrorCode.ERR_PASSWORD_ERROR)

        code, msg = user.auth("c4pt01r@126.com", "shit")
        self.assertEqual(code, user.UserErrorCode.ERR_PASSWORD_ERROR)


    def tearDown(self):
        db_utils.db.drop_collection('user')
        pass
