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
import cgi

def shift_n_letters(letter, n):
    n%=26
    c=ord(letter)
    c=c+n
    if c>ord('z'):
        e=c-ord('z')
        c=ord('a')+e-1
    elif c<ord('a'):
        e=ord('a')-c
        c=ord('z')-e
    return chr(c)

def rot13(x):
    news=""
    for i in x:
        if not i.isalpha():
            news+=i
        else:
            if i.islower():
                news+=shift_n_letters(i,13)
            else:
                news+=shift_n_letters(i.lower(),13).upper()
    return cgi.escape(news,quote=True)

form="""
<html>
<head><title>ROT13 Encryption</title></head>
<body>
    <form action="" method="post">
        <h1>Enter some test to ROT13:</h1>
        <textarea rows="5" cols="100" name="text" placeholder="Enter some text here:">%(t)s</textarea>
        <br>
        <input type="submit">
    </form>
</body>
</html>
"""

signup="""
<!DOCTYPE html>

<html>
  <head>
    <title>Sign Up</title>
    <style type="text/css">
      .label {text-align: right}
      .error {color: red}
    </style>

  </head>

  <body>
    <h2>Signup</h2>
    <form method="post">
      <table>
        <tr>
          <td class="label">
            Username
          </td>
          <td>
            <input type="text" name="username" value="%(username)s">
          </td>
          <td class="error">
            %(unerror)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Password
          </td>
          <td>
            <input type="password" name="password" value="">
          </td>
          <td class="error">
            %(perror)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Verify Password
          </td>
          <td>
            <input type="password" name="verify" value="">
          </td>
          <td class="error">
            %(vperror)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Email (optional)
          </td>
          <td>
            <input type="text" name="email" value="%(email)s">
          </td>
          <td class="error">
            %(eerror)s
          </td>
        </tr>
      </table>

      <input type="submit">
    </form>
  </body>

</html>"""

import re
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def isValid(q,p):
    return q.match(p)

class SignupHandler(webapp2.RequestHandler):
    une,pe,vpe,ee="","","",""
    def get(self):
        self.response.write(signup%{"username":"",
                                    "unerror":self.une,
                                    "perror":self.pe,
                                    "vperror":self.vpe,
                                    "email":"",
                                    "eerror":self.ee})

    def post(self):
        un=self.request.get("username")
        p=self.request.get("password")
        vp=self.request.get("verify")
        e=self.request.get("email")
        if not isValid(USER_RE,un):
            self.une="That's not a valid username."
        if not isValid(PASSWORD_RE,p):
            self.pe="That wasn't a valid password."
        if p!=vp:
            self.vpe="Your passwords didn't match."
        if not isValid(EMAIL_RE,e):
            self.ee="That's not a valid email."

        if not self.une and not self.pe and not self.vpe and not self.ee:
            rdpage="/unit2/welcome?username="+un
            self.redirect(rdpage)
        else:
            self.response.write(signup%{"username":cgi.escape(un,quote=True),
                                        "unerror":self.une,
                                        "perror":self.pe,
                                        "vperror":self.vpe,
                                        "email":cgi.escape(e,quote=True),
                                        "eerror":self.ee})

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        u=self.request.get("username")
        self.response.write("Welcome, "+u+"!")

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("Hello, Udacity!")

class ROT13Handler(webapp2.RequestHandler):
    def get(self):
        self.response.write(form%{"t":""})
    def post(self):
        t=self.request.get("text")
        t=rot13(t)
        self.response.write(form%{"t":t})


app = webapp2.WSGIApplication([
    ('/',MainHandler),
    ('/unit2/rot13', ROT13Handler),
    ('/unit2/signup',SignupHandler),
    ('/unit2/welcome',WelcomeHandler)
], debug=True)
