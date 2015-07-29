from google.appengine.ext import ndb

class User(ndb.Model):
    name = StringProperty(required = True)

class Video(ndb.Model):
    identifaction = StringProperty()
    duration = IntergerProperty()
    title = StringProperty()
    image = StringProperty()
    genre = StringProperty()

class UserVideo(ndb.Model):
    user_key = KeyProperty()
    video_key = KeyProperty()
