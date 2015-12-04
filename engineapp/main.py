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

form='''
<h1>Yo Google Search!</h1>
<form action="https://www.google.com/search">
    <input type="text" name="q">
    <input type="submit">
</form>
<h1>Yo See the request! Get!</h1>
<form action="/search">
    <input type="text" name="q">
    <input type="submit">
</form>
<h1>Yo See the request! Post!</h1>
<form action="/search" method="post">
    <input type="text" name="q">
    <input type="submit">
</form>
'''

bdayform='''
<form method="post">
    What is your birthday?
    <br />
    <input type="text" name="month" placeholder="Month">
    <input type="text" name="day" placeholder="Day">
    <input type="text" name="year" placeholder="Year">

    <br />
    <br />
    <input type="submit">
</form>
'''

months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']

def valid_month(month):
    if month:
        month=month[0].upper()+month[1:].lower()
        if month not in months:
            return None
        return month
    return None


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(bdayform)
    def post(self):
        self.response.write("Thanks! Thats a totally valid day!")

class MyHandler(webapp2.RequestHandler):
    def post(self):
        #q=self.request.get("q")
        self.response.headers['Content-Type']='text/plain'
        self.response.out.write(self.request)
        #self.response.write("</br>404 Error <br /> Not Found '"+q+"'")
    def get(self):
        self.response.headers['Content-Type']='text/plain'
        self.response.out.write(self.request)

app = webapp2.WSGIApplication([
    ('/', MainHandler),('/search', MyHandler)
], debug=True)
