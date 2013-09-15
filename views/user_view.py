import tornado.web
import router
import models.user as user

@router.route("/user/login")
class UserLoginHandler(tornado.web.RequestHandler):
    def get(self):
       self.write("tes1t")
       pass 
