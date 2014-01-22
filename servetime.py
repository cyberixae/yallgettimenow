import cgi
import os
import time
import urllib
import logging
import pickle

from django.utils import simplejson as json

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import memcache

# Set the debug level
_DEBUG = True
    
class MainPage(webapp.RequestHandler):
  def get(self):
    self.response.out.write('''<!DOCTYPE html>
<html>
<head>
  <title>Y'all Get Time Now</title>
</head>
<body>
  <h1>Y'all Get Time Now</h1>
  <p>
    <a href="/gettimenow">text</a>
    <a href="/gettimenow?format=json">json</a>
    <a href="/gettimenow?format=xml">xml</a>
  </p>
</body>
</html>''');

class TimePage(webapp.RequestHandler):
  
  def _send_text(self, millis):
      unitime = unicode(millis)
      strtime = str(unitime)
      self.response.headers['Content-Type'] = 'text/plain; charset=utf-8'
      self.response.out.write(strtime);
  
  def _send_json(self, millis):
      jsontime = json.dumps(millis)
      self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
      self.response.out.write(jsontime);
  
  def _send_xml(self, millis):
      unitime = unicode(millis)
      xmltime = '<?xml version="1.0"?><time>' + str(unitime) + '</time>'
      self.response.headers['Content-Type'] = 'application/xml; charset=utf-8'
      self.response.out.write(xmltime);
      
  def get(self):
      output_format = self.request.get('format', allow_multiple=False)
      seconds = time.time()
      millis = int(seconds * 1000)
      if output_format == '':
          self._send_text(millis)
      elif output_format == 'json':
          self._send_json(millis)
      elif output_format == 'xml':
          self._send_xml(millis)
      else:
          assert False
      

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/gettimenow', TimePage)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()