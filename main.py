from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util

import logging
import os

class MainPageHandler(webapp.RequestHandler):
	def get(self):
		path = os.path.join(os.path.dirname(__file__), 'static', 'theAbode.html')
		logging.info("Path is %s" % path)
		self.response.out.write(template.render(path, {}, debug=True))


application = webapp.WSGIApplication([('/', MainPageHandler), ('/theAbode.html', MainPageHandler)], debug = True)
def main():
	util.run_wsgi_app(application)


if __name__ == '__main__':
	main()
