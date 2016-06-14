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

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir) , autoescape = True)



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


   
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/rot13' , ROT13Handler)
], debug=True)
