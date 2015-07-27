import jinja2
import os
import urllib
import webapp2

from apiclient.discovery import build

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

REGISTRATION_INSTRUCTIONS = """
    You must set up a project and get an API key to run this code. <br>
    Steps: <br>
    1.  Visit <a href="https://developers.google.com/youtube/v3/code_samples/python_appengine#create-api-key"
    target='_top'>https://developers.google.com/youtube/v3/code_samples/python_appengine#create-api-key</a>
    for instructions on setting up a project and key. Make sure that you have
    enabled the YouTube Data API (v3) for your project.
    You do not need to set up OAuth credentials for this project. <br>
    2.  Once you have obtained a key, search for the text 'REPLACE_ME' in the
    code and replace that string with your key. <br>
    3.  Click the reload button above the output container to view the new output. """

# Set API_KEY to the "API key" value from the "Access" tab of the
# Google APIs Console http://code.google.com/apis/console#access
# Please ensure that you have enabled the YouTube Data API and Freebase API
# for your project.
API_KEY = "AIzaSyAx04A3kgr6A6WmICcFAjwcecSPOTKocIY"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
QUERY_TERM = "dog"

class MainHandler(webapp2.RequestHandler):
  def get(self):
    if API_KEY == "REPLACE_ME":
      self.response.write(REGISTRATION_INSTRUCTIONS)
    else:
      #Present a list of videos associated with the keyword
      self.search_by_keyword()

  def search_by_keyword(self):
    youtube = build(
      YOUTUBE_API_SERVICE_NAME,
      YOUTUBE_API_VERSION,
      developerKey=API_KEY
    )
    search_response = youtube.search().list(
      q=QUERY_TERM,
      part="id,snippet",
      maxResults=5
    ).execute()

    videos = []

    for search_result in search_response.get("items", []):
      videos.append(search_result)

    template_values = {
      'videos': videos
    }

    self.response.headers['Content-type'] = 'text/html'
    template = JINJA_ENVIRONMENT.get_template('index.html')
    self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
  ('/.*', MainHandler),
], debug=True)
