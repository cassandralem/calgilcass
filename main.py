
import webapp2
import os
import jinja2

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("templates/home.html")
        self.response.write(template.render())

class NewVideoHandler(webapp2.RequestHandler):
    def post(self):

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
