import logging
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
    like_count = ndb.IntegerProperty(default = 0)

def add_default_videos():
    cat = Photo(user_name='Cat', video_id='tntOCGkgt98', like_count=0)
    llama = Photo(user_name='Llama', video_id='KG1U8-i1evU', like_count=0)

    cat.put()
    llama.put()

    return [llama, cat]

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("templates/home.html")
        video_query = UploadedVideo.query().order(UploadedVideo.post_time)
        videos = video_query.fetch()

        template_vars = {
        "videos": videos
        }

        self.response.write(template.render(template_vars))

    #def post(self):
        #video_query = UploadedVideo.query().order(UploadedVideo.post_time)
        #videos = video_query.fetch()

        #self.redirect('/')

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

        new_video = UploadedVideo(user_name=user_name, video_id=video_id, like_count = 0)
        new_video.put()

        self.redirect('/newvideo')

class LikeHandler(webapp2.RequestHandler):
    # Handles increasing the likes when you click the button.
    def post(self):

        # === 1: Get info from the request. ===
        urlsafe_key = self.request.get('video_key')

        # === 2: Interact with the database. ===

        # Use the URLsafe key to get the video from the DB.
        video_key = ndb.Key(urlsafe=urlsafe_key)
        video = video_key.get()

        # Fix the photo like count just in case it is None.
        if video.like_count == None:
            video.like_count = 0

        # Increase the photo count and update the database.
        video.like_count = video.like_count + 1
        video.put()

        # === 3: Send a response. ===
        # Send the updated count back to the client.
        self.response.write(video.like_count)

class GetAndDeleteVideoHandler(webapp2.RequestHandler):
    def post(self):
        urlsafe_key = self.request.get('videoUrl')
        videoUrl = ndb.Key(urlsafe = urlsafe_key)
        video_id = videoUrl.get()

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/about', AboutHandler),
    ('/newvideo', NewVideoHandler),
    ('/likes', LikeHandler),
    ('/getdeletevideo', GetAndDeleteVideoHandler)
], debug=True)
