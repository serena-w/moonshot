#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import urllib
import isodate
import datetime
from google.appengine.ext import ndb
from google.appengine.api import users
from apiclient.discovery import build

env = jinja2.Environment(loader = jinja2.FileSystemLoader('templates'))

API_KEY = "AIzaSyAx04A3kgr6A6WmICcFAjwcecSPOTKocIY"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
QUERY_TERM = "dog"

class Search(ndb.Model):
    time = ndb.IntegerProperty(required=True)
    genre = ndb.StringProperty()

class SearchHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        login_url = ''
        logout_url = ''
        email = ''
        if user:
            email = user.email()
            logout_url = users.create_logout_url('/')
        else:
            login_url = users.create_login_url('/')
        template = env.get_template('main.html')
        variables = {}
        self.response.write(template.render(variables))
    """
    def post(self):
        time = int(self.request.get("time"))
        search = Search(time=time)
        search.put()
        results = Results(search)
        template = env.get_template('results.html')
        variables = {'link': results.results[0]}
        self.response.write(template.render(variables))
    """

    def convert_time(self, duration):
        duration_time = isodate.parse_duration(duration)
        print duration
        print duration_time.total_seconds()
        return duration_time.total_seconds()

    def post(self):
        youtube = build(
            YOUTUBE_API_SERVICE_NAME,
            YOUTUBE_API_VERSION,
            developerKey=API_KEY
          )
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
        if time<360:
            time_category = "short"
        elif time<3600:
            time_category="medium"
        else:
            time_category="long"
        print "TIME:"
        print time
        search_response = youtube.search().list(
            q=QUERY_TERM,
            part="id, snippet",
            maxResults=10,
            type="video",
            videoDuration=time_category
          ).execute()

        search_videos = []

        for search_result in search_response.get("items", []):
            search_videos.append(search_result["id"]["videoId"])
        video_ids = ",".join(search_videos)

        # Call the videos.list method to retrieve duration data for each video
        video_response = youtube.videos().list(
            id=video_ids,
            part="id, snippet, contentDetails"
        ).execute()

        videos = []

        # Add each result to the list
        for video_result in video_response.get("items", []):
            video_duration =  self.convert_time(video_result["contentDetails"]["duration"])
            if video_duration <= time:
                print "ADDING VIDEO"
                videos.append([video_result, datetime.timedelta(seconds=video_duration)])

        template_values = {
            'videos': videos
        }

        template = env.get_template('index.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/', SearchHandler),
    ('/search', SearchHandler),
], debug=True)
