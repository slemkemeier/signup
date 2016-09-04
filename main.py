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
import re
import jinja2
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))




class MainHandler(Handler):
    def valid_username(self, username):
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        if USER_RE.match(username):
            return username
        else:
            return ""

    def valid_password(self, password):
        PASSWORD_RE = re.compile(r"^.{3,20}$")
        if PASSWORD_RE.match(password):
            return password
        else:
            return ""

    def valid_email(self, email):
        EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
        if not email:
            return ""
        if EMAIL_RE.match(email):
            return email

    def valid_verify(self, password, verify):
        if password == verify:
            return verify

    def writeForm(self, username="", email="", username_error="", pass_error="",
                    verify_error="", email_error=""):
        self.render('signup_tem.html', username=username, email=email,
                    username_error=username_error, pass_error=pass_error,
                    verify_error=verify_error, email_error=email_error)

    def get(self):
        self.writeForm()

    def post(self):
        username_error = ""
        pass_error = ""
        verify_error = ""
        email_error = ""
        error = False

        user_username = self.request.get("username")
        user_password = self.request.get("password")
        user_verify = self.request.get("verify")
        user_email = self.request.get("email")

        username = self.valid_username(user_username)
        password = self.valid_password(user_password)
        verify = self.valid_verify(user_password, user_verify)
        email = self.valid_email(user_email)

        if (username and password and verify and (email is not None)):
            self.redirect("/welcome?username=%(username)s" %{"username":user_username})

        else:
            if not username:
                username_error="That's not a valid username."
            if not password:
                pass_error="That's not a valid password."
            if not email and (email is None):
                email_error="That's not a valid email."
            if not verify:
                verify_error="That password does not match."
            self.writeForm(user_username, user_email, username_error,
                            pass_error, verify_error, email_error)


class WelcomeHandler(Handler):
    def get(self):
        username = self.request.get("username")
        self.response.out.write("Welcome, %s" %username)



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
