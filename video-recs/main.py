import webapp2 #library we use to connect our app with our handlers
import jinja2 #library for linking our script with our templates
from google.appengine.ext import ndb #module to interact with datastore
from google.appengine.api import users #module to work with user accounts
from apiclient.discovery import build #module to work with YouTube API
import youtube
import random

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
        vid_list = ['/static/snow.mp4', '/static/sea.mp4', '/static/test.mp4']
        x = random.randint(0, len(vid_list) - 1)
        current_video = vid_list[x]
        if user:
            email = user.email()
            logout_url = users.create_logout_url('/')
        else:
            login_url = users.create_login_url(self.request.uri)
        template = env.get_template('main.html')
        variables = {"logout_url":logout_url,"login_url":login_url, 'current_video': current_video}
        self.response.write(template.render(variables))




    def post(self):
    # renders results page, calls on youtube module to do search and get video attributes
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
            'videos': videos
        }

        template = env.get_template('results.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/', SearchHandler),
    ('/search', SearchHandler),
], debug=True)
