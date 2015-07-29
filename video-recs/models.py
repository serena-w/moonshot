from google.appengine.ext import ndb

class User(ndb.Model):
    name = ndb.StringProperty(required = True)

class Video(ndb.Model):
    user_key = ndb.KeyProperty(required = True)
    vid_id = ndb.StringProperty()
    added_date = ndb.DateTimeProperty(auto_now_add = True)
