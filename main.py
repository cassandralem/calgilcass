import logging
import webapp2
import os
import jinja2
import json

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

from google.appengine.ext import ndb

class UploadedVideo(ndb.Model):
    user_name = ndb.StringProperty()
    video_id = ndb.StringProperty()
    post_time = ndb.DateTimeProperty(auto_now_add=True)
    like_count = ndb.IntegerProperty(default = 0)
    played = ndb.BooleanProperty(default = False)

class CurrentVideos(ndb.Model):
    video_right_key = ndb.KeyProperty(kind=UploadedVideo)
    video_left_key = ndb.KeyProperty(kind=UploadedVideo)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("templates/home.html")
        video_query = UploadedVideo.query().order(UploadedVideo.post_time)
        videos = video_query.fetch()

        current_query = CurrentVideos.query()
        playing_videos = current_query.get()

        left_key = playing_videos.video_left_key
        right_key = playing_videos.video_right_key

        left_vid = left_key.get()
        right_vid = right_key.get()

        left_id = left_vid.video_id
        right_id = right_vid.video_id

        url_safe_right = right_vid.key.urlsafe()
        url_safe_left = left_key.urlsafe()

        logging.info(url_safe_right)
        logging.info(url_safe_left)

        video_query = UploadedVideo.query().order(UploadedVideo.post_time).filter(UploadedVideo.played==False)
        unplayedVideos = video_query.fetch()

        template_vars = {
        "videos": videos,
        "unplayedVideos": unplayedVideos,
        "left_id": left_id,
        "right_id": right_id,
        "left_key": left_key,
        "right_key": right_key,
        "left_urlsafe": url_safe_left,
        "right_urlsafe": url_safe_right,
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

class InitializeDefaultsHandler(webapp2.RequestHandler):
    def get(self):
        video_query = UploadedVideo.query().filter().order(UploadedVideo.post_time)
        videos = video_query.fetch()
        current_query = CurrentVideos.query()
        playing_videos = current_query.get()

        for video in videos:
            video.key.delete()

        default1 = UploadedVideo(user_name='D1', video_id='3XwKepsOjKA', played=True)
        default2 = UploadedVideo(user_name='D2', video_id='ZXsQAXx_ao0', played=True)
        default3 = UploadedVideo(user_name='D3', video_id='o0u4M6vppCI')
        default4 = UploadedVideo(user_name='D4', video_id='oYmPJfMCsvc')
        default5 = UploadedVideo(user_name='D5', video_id='3aQRO29ZzbE')
        default6 = UploadedVideo(user_name='D6', video_id='dGinm6KIC4Q')
        default7 = UploadedVideo(user_name='D7', video_id='zOVPlw_QC1o')
        default8 = UploadedVideo(user_name='D8', video_id='zGcYabz3hYg')
        default9 = UploadedVideo(user_name='D9', video_id='_-47JOTCXGQ')
        default10 = UploadedVideo(user_name='D10', video_id='KzARx0EuDgc')
        default11 = UploadedVideo(user_name='D11', video_id='wej-t_as93Q')
        default12 = UploadedVideo(user_name='D12', video_id='3XyOgx9bCUo')
        default13 = UploadedVideo(user_name='D13', video_id='lLWEXRAnQd0')
        default14 = UploadedVideo(user_name='D14', video_id='0_jBz6eN-Ew')
        default15 = UploadedVideo(user_name='D15', video_id='oN-KOoVuhuo')
        default16 = UploadedVideo(user_name='D16', video_id='k9xronkrgng')

        default1.put()
        default2.put()
        default3.put()
        default4.put()
        default5.put()
        default6.put()
        default7.put()
        default8.put()
        default9.put()
        default10.put()
        default11.put()
        default12.put()
        default13.put()
        default14.put()
        default15.put()
        default16.put()

        playing_videos.key.delete()
        playing_videos = CurrentVideos(video_right_key=default1.key, video_left_key=default2.key)
        playing_videos.put()

        print "final playing_videos:", playing_videos
        self.redirect('/')


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
    def get(self):
        print "HELLO"
    def post(self):
        current_query = CurrentVideos.query()
        playing_videos = current_query.get()

        video_query = UploadedVideo.query().filter(UploadedVideo.played==False).order(UploadedVideo.post_time)
        video = video_query.get()
        video.played = True
        video.put()

        print "Initial playing_videos:", playing_videos

        video_right_key = playing_videos.video_right_key
        video_left_key = playing_videos.video_left_key

        right_video = video_right_key.get()
        left_video = video_left_key.get()
#need to change likes
        logging.info(right_video.like_count)
        logging.info(left_video.like_count)

        if right_video.like_count > left_video.like_count:
            print "right_video.like_count > left_video.like_count"
            playing_videos.video_left_key = video.key
            left_video = video
            # logging.info(left_video)
            right_video.like_count = 0
            right_video.put()
            left_video.put()
        elif right_video.like_count <= left_video.like_count:
            print "right_video.like_count <= left_video.like_count"
            playing_videos.video_right_key = video.key
            right_video = video
            # logging.info(right_key)
            left_video.like_count = 0
            left_video.put()
            right_video.put()
        else:
            print "THIS SHOULD NOT HAPPEN!"

        playing_videos.put()
        print "Final playing_videos:", playing_videos



            # video_query2 = UploadedVideo.query().filter(UploadedVideo.played==True).order(-UploadedVideo.post_time)
            # lastvid = video_query2.get()
            #
            # lastvid.like_count = 0

        # lastvid.put()
        response_vars = {
            "videoIdRight": right_video.video_id,
            "videoUrlSafeKeyRight": right_video.key.urlsafe(),
            "videoIdLeft": left_video.video_id,
            "videoUrlSafeKeyLeft": left_video.key.urlsafe()
        }

        print "response_vars", response_vars

        # TODO: Write a JSON response with the JSONified dictionary of the id and URLSafeKey
        self.response.write(json.dumps(response_vars))



        #if videos == None:
            #add_default_videos()
        # for video in videos:
        #     if video.played == False:
        #         self.response.write(video.video_id)
        #         video.played = True
        #         break
        #     elif video.played == True:
        #         video.key.delete



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/about', AboutHandler),
    ('/newvideo', NewVideoHandler),
    ('/likes', LikeHandler),
    ('/getdeletevideo', GetAndDeleteVideoHandler),
    ('/defaults', InitializeDefaultsHandler),

], debug=True)
