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
from google.appengine.ext import ndb
from google.appengine.api import users

env = jinja2.Environment(loader = jinja2.FileSystemLoader('template'))

class MainHandler(webapp2.RequestHandler):
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

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
