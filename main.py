
import webapp2
import os
import jinja2

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

from google.appengine.ext import ndb

class UploadedVideo(ndb.Model):
    user_name = ndb.StringProperty()
    video_id = ndb.StringProperty()
    post_time = ndb.DateTimeProperty(auto_now_add=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("templates/home.html")
        video_query = UploadedVideo.query().order(UploadedVideo.post_time)
        videos = video_query.fetch()

        template_vars = {
        "videos": videos
        }

        self.response.write(template.render(template_vars))

    def post(self):
        video_query = UploadedVideo.query().order(UploadedVideo.post_time)
        videos = video_query.fetch()

        videos[0].key.delete()
        self.redirect('/')

class AboutHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("templates/about.html")
        self.response.write(template.render())

class NewVideoHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("templates/newvideo.html")
        self.response.write(template.render())
    def post(self):
        user_name = self.request.get('user_name')
        video_id = self.request.get('video_id')

        new_video = UploadedVideo(user_name=user_name, video_id=video_id)
        new_video.put()

        self.redirect('/newvideo')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/about', AboutHandler),
    ('/newvideo', NewVideoHandler)

], debug=True)
