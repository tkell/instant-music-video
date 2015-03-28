# TODO:  autosharing, FB meta tags, etc etc etc
# TODO:  Error catching

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

import cgi
import oembed
import os
import re

def sc_embed_helper(sc_url):
	consumer = oembed.OEmbedConsumer()

	sc_endpoint = oembed.OEmbedEndpoint('http://soundcloud.com/oembed', ['http://soundcloud.com/*/*'])
	consumer.addEndpoint(sc_endpoint)
	sc_response = consumer.embed(sc_url + "&auto_play=true&color=111111&show_comments=false")
	
	return sc_response['html']
	
def make_permalink(v_url, sc_url):
	url = "http://instantmusicvideo.appspot.com/" + "?v_url=" + v_url + "&sc_url=" + sc_url
	return "<a href=" + url + "> link to this music video.</a>"

class MainPage(webapp.RequestHandler):    		
    def get(self):
    	try:
	    	video_url = self.request.get("v_url")
	    	sc_url = self.request.get("sc_url")
    		
	    	s_embed_html = ''
	    	v_id = ''
	    	y_id = ''

    	
	    	permalink = ''
	    	if video_url != '' and sc_url != '':
	    		if 'vimeo.com' in video_url:
	    			v_id = re.search('\.com/(\d+)', video_url).group(1)
	    		elif 'youtube.com' in video_url:
	    			y_id = "'" + re.search('\.com/watch\?v=(.+)', video_url).group(1) + "'"
	    		# Temp version for Andrew
	    		elif 'reels.sohosoho.tv/embed/' in video_url:
	    			ss_id = re.search('\.tv/embed/(.*)', video_url).group(1)
	    			ss_text = '''<object width="640" height="360">
	    						 <param name="movie" value="http://reels.sohosoho.tv/embed/white/autoplay/%s"></param>
								 <param name="allowFullScreen" value="true"></param>
							     <param name="allowscriptaccess" value="always"></param>
								 <embed src="http://reels.sohosoho.tv/embed/white/autoplay/%s" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="640" height="360"></embed>
								 </object>''' % (ss_id, ss_id)

	    		sc_embed_html = sc_embed_helper(sc_url)
	    		permalink = make_permalink(video_url, sc_url)
	    	else:
	    		v_id = '8837024'
	    		y_id = ''
	    		ss_text = ''
	    		sc_embed_html = sc_embed_helper('http://soundcloud.com/forss/flickermood')
	    		video_url = 'http://vimeo.com/...'
	    		sc_url = 'http://soundcloud.com/.../...'
	    		permalink = make_permalink('http://vimeo.com/8837024', 'http://soundcloud.com/forss/flickermood')
	
	        template_values = {
	        				'v_id' : v_id,
	        				'y_id' : y_id,
	        				'ss_text' : ss_text,
							'sc_embed_html' : sc_embed_html,
	        				'v_url' : video_url,
	        				'sc_url' : sc_url,
	        				'permalink'  : permalink,
	        				}
	    	path = os.path.join(os.path.dirname(__file__), 'index.html')
        	self.response.out.write(template.render(path, template_values)) 
           				
        except:
    		template_values = {	
					'v_url' : "http://vimeo.com/...",
					'sc_url' : "http://soundcloud.com/.../...",
					}
    		path = os.path.join(os.path.dirname(__file__), '404.html')
    		self.response.out.write(template.render(path, template_values))		
    	

	        
    def post(self):
    	try:
	    	video_url = self.request.get("v_url")
	    	sc_url = self.request.get("sc_url")
	
	    	v_id = ''
	    	y_id = ''
	    	ss_text = ''
	    	
	    	if 'vimeo.com' in video_url:
	    		v_id = re.search('\.com/(\d+)', video_url).group(1)
	    	elif 'youtube.com' in video_url:
	    		y_id = "'" + re.search('\.com/watch\?v=(.+)', video_url).group(1) + "'" # youtube requires explicit single quotes.
	    	# Temp version for Andrew
	    	elif 'reels.sohosoho.tv/embed/' in video_url:
	    		ss_id = re.search('\.tv/embed/(.*)', video_url).group(1)
    			ss_text = '''<object width="640" height="360">
			 				<param name="movie" value="http://reels.sohosoho.tv/embed/white/autoplay/%s"></param>
			 				<param name="allowFullScreen" value="true"></param>
		     				<param name="allowscriptaccess" value="always"></param>
			 				<embed src="http://reels.sohosoho.tv/embed/white/autoplay/%s" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="640" height="360"></embed>
							</object>''' % (ss_id, ss_id)
	    	sc_embed_html = sc_embed_helper(sc_url)
	    	
	    	permalink = make_permalink(video_url, sc_url)
	    	
	        template_values = {	
					'v_id' : v_id,
					'y_id' : y_id, 
					'ss_text' : ss_text,
					'sc_embed_html' : sc_embed_html,
					'v_url' : video_url,
					'sc_url' : sc_url,
					'permalink'  : permalink,
					}
    		path = os.path.join(os.path.dirname(__file__), 'index.html')
    		self.response.out.write(template.render(path, template_values))
					
        except:
    		template_values = {	
					'v_url' : "http://vimeo.com/...",
					'sc_url' : "http://soundcloud.com/.../...",
					}
    		path = os.path.join(os.path.dirname(__file__), '404.html')
    		self.response.out.write(template.render(path, template_values))		
					

				
application = webapp.WSGIApplication(
                                     [('/', MainPage), ('/index.html', MainPage)],
                                     debug=True)
	
def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
    