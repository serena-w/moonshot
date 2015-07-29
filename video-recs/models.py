from google.appengine.ext import ndb

class User(ndb.Model):
    name = ndb.StringProperty(required = True)

class Video(ndb.Model):
    user_key = ndb.KeyProperty()
    vid_id = ndb.StringProperty()
    duration = ndb.IntegerProperty()
    title = ndb.StringProperty()
    image = ndb.StringProperty()
    genre = ndb.StringProperty()
