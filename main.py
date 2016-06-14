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

import os
import webapp2
import jinja2
import re

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir) , autoescape = True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params ):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw ):
        self.write(self.render_str(template , **kw))



class MainHandler(Handler):
    def get(self):
        items = self.request.get_all("food")
        self.render("shopping_list.html" , items=items)

class ROT13Handler(Handler):
    def get(self):
        rot13txAr = self.rot13fy(self.request.get("rot13txAr"))
        #rot13txAr = "Vinodh"
        self.render("rot13.html" , rot13txAr=rot13txAr)

    def rot13fy(self,s):
        #Convert the Input String to ASCII Chars
        inputToASCIIList = [ord(c) for c in s]
        # Final Output will be rendered in this list
        finalASCIIList = []
        # Iterate the generated ASCII list
        for alphas in inputToASCIIList:
            # if Upper lower case enter here
            if (97 <= alphas <= 122):
                # If the arrived number is not with in the 122 limit
                # Circle back to the beginning of 97
                if alphas + 13 > 122:
                    moveTo = 97 + ((alphas + 13) - 122) - 1
                    finalASCIIList.append(moveTo)
                # If its well within limits do the below
                else :
                    finalASCIIList.append(alphas + 13)
            # Same Logic applies to Lower her too
            elif(65 <= alphas <= 90):
                if alphas + 13 > 90:
                    moveTo = 65 + ((alphas + 13) - 90) - 1
                    finalASCIIList.append(moveTo)
                else :
                    finalASCIIList.append(alphas + 13)
            #If its not an alphabet then just put the ASCII char as such in the list
            else :
                finalASCIIList.append(alphas)
        #Convert the Array to String
        return ''.join(chr(i) for i in finalASCIIList)

class UserSignUpHandler(Handler):
    def get(self):
        self.render("userSignUp.html")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        usernameErr = False
        passwordErr = False
        verifyPassErr = False
        verfiyErr = False
        emailErr = False


        if self.valid_username(username) is None:
            usernameErr = True
        if self.valid_password(password) is None:
            passwordErr = True
        if self.valid_password(verify) is None:
            verfiyErr = True
        if not self.valid_matching_password(password,verify):
            verifyPassErr = True
        if email:
            if self.valid_email(email) is None:
                emailErr = True

        if usernameErr or passwordErr or verifyPassErr or verfiyErr or emailErr:
            self.render("userSignUp.html" , username=username , email=email , usernameErr=usernameErr,
            passwordErr=passwordErr , verifyPassErr=verifyPassErr,verfiyErr=verfiyErr,emailErr=emailErr)
        else:
            self.redirect("thanks?username="+str(username))
  
    def valid_username(self,username):
        return USER_RE.match(username)

    def valid_password(self,password):
        return USER_RE.match(password)

    def valid_matching_password(self,password,verify):
        return password == verify

    def valid_email(self,email):
        return EMAIL_RE.match(email)
        
class ThanksHandler(Handler):
    def get(self):
        username = self.request.get("username")
        self.render("thanks4SignUp.html" , username=username)


   
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/rot13' , ROT13Handler),
    ('/signUp' , UserSignUpHandler),
    ('/thanks', ThanksHandler)
], debug=True)
