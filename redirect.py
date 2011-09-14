from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util

import logging
import os


class PlusProfilePageHandler(webapp.RequestHandler):
  def get(self):
    self.redirect('https://profiles.google.com/adewale/about', permanent=True)

# Set up a redirect to my Google Plus Profile page
# The %2B maps to /+
application = webapp.WSGIApplication([('/%2B', PlusProfilePageHandler)], debug = True)
def main():
	util.run_wsgi_app(application)


if __name__ == '__main__':
	main()