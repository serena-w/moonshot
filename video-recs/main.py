import webapp2 #library we use to connect our app with our handlers
import jinja2 #library for linking our script with our templates
from google.appengine.ext import ndb #module to interact with datastore
from google.appengine.api import users #module to work with user accounts
from apiclient.discovery import build #module to work with YouTube API
import youtube
import random
import models

# global variable that stores the configuration and global objects
# uses the FileSystemLoader to lad template files from the folder "templates"
env = jinja2.Environment(loader = jinja2.FileSystemLoader('templates'))

class SearchHandler(webapp2.RequestHandler):
    """
    Renders main page when get() function is called and results page when post()
    function is called by the main page form
    """
    def get(self):
    # renders main page
    # will be improved to pass login and logout url's and user information to main page template
        user = users.get_current_user()
        login_url = ''
        logout_url = ''
        email = ''
        vid_list = ['/static/snow.mp4', '/static/bluemotion.mp4','/static/rain.mp4','/static/sun.mp4']
        x = random.randint(0, len(vid_list) - 1)
        current_video = vid_list[x]
        if user:
            user_key = ndb.Key('User', user.email())
            check_user = models.User.query(models.User.key == user_key).fetch()
            if check_user == []:
                new_user = models.User(name=user.nickname(), id=user.email())
                new_user.put()
            logout_url = users.create_logout_url('/')
        else:
            login_url = users.create_login_url(self.request.uri)
        template = env.get_template('main.html')
        variables = {"logout_url":logout_url,"login_url":login_url, 'current_video': current_video}
        self.response.write(template.render(variables))




    def post(self):
    # renders results page, calls on youtube module to do search and get video attributes
        user = users.get_current_user()
        login_url = ''
        logout_url = ''
        email = ''
        redirect_url = users.create_login_url('/')
        if user:
            user_key = ndb.Key('User', user.email())
            check_user = models.User.query(models.User.key == user_key).fetch()
            if check_user == []:
                new_user = models.User(name=user.nickname(), id=user.email())
                new_user.put()
                user_key = ndb.Key('User', user.email())
            logout_url = users.create_logout_url('/')
        else:
            login_url = users.create_login_url(self.request.uri)
        hours = self.request.get("HOURS")
        if hours=="":
            hours = 0
        else:
            hours = int(hours)
        minutes = self.request.get("MINUTES")
        if minutes=="":
            minutes = 0
        else:
            minutes = int(minutes)
        seconds = self.request.get("SECONDS")
        if seconds=="":
            seconds = 0
        else:
            seconds = int(seconds)

        time = (hours*3600) + (minutes*60) + (seconds)

        videos = youtube.search(time, self.request.get_all("genre"))

        template_values = {
            'videos': videos, 'login_url':login_url, 'logout_url':logout_url, 'redirect_url':redirect_url
        }

        template = env.get_template('results.html')
        self.response.write(template.render(template_values))

class SavedVideosHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('saved_videos.html')
        user = users.get_current_user()
        if user:
            user_key = ndb.Key('User', user.email())
            check_user = models.User.query(models.User.key == user_key).fetch()
            if check_user == []:
                new_user = models.User(name=user.nickname(), id=user.email())
                new_user.put()

            logout_url = users.create_logout_url('/')
            saved_vids = models.Video.query(models.Video.user_key == user_key).order(-models.Video.added_date).fetch()
            template_data = {'videos':saved_vids}
            self.response.write(template.render(template_data))
        else:
            login_url = users.create_login_url(self.request.uri)
            self.redirect(login_url)

    def post(self):
        vids = self.request.get_all('video_info')
        user = users.get_current_user()
        if user:
            user_key = ndb.Key('User', user.email())
            check_user = models.User.query(models.User.key == user_key).fetch()
            if check_user == []:
                new_user = models.User(name=user.nickname(), id=user.email())
                new_user.put()
                user_key = ndb.Key('User', user.email())
            logout_url = users.create_logout_url('/')
            for vid in vids:
                vid_key = ndb.Key('Video', vid+user.email())
                check_vid = models.Video.query(models.Video.key == vid_key).fetch()
                if check_vid == []:
                    saved_vid = models.Video(user_key = user_key,vid_id = vid, id=(vid+user.email()))
                    saved_vid.put()
            template = env.get_template('saved_videos.html')
            videos = models.Video.query(models.Video.user_key == user_key).order(-models.Video.added_date).fetch()
            template_data = {"videos": videos}
            self.response.write(template.render(template_data))
        else:
            login_url = users.create_login_url('/')
            self.redirect(login_url)



app = webapp2.WSGIApplication([
    ('/', SearchHandler),
    ('/search', SearchHandler),
    ('/save', SavedVideosHandler),
    ('/saved_videos', SavedVideosHandler)
], debug=True)
