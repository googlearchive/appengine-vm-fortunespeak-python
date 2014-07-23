import webapp2
import subprocess

MESSAGES = '/tmp/messages.txt'

class HelloHandler(webapp2.RequestHandler):
  def get(self):
    msg = subprocess.check_output('/usr/games/fortune')
    with open(MESSAGES, 'a') as f: f.write(msg)
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write(msg)

class MessagesHandler(webapp2.RequestHandler):
  def get(self):
    with open(MESSAGES, 'r') as f:
      for msg in f: self.response.out.write(msg)

app = webapp2.WSGIApplication([('/', HelloHandler),
                               ('/messages', MessagesHandler)],
                               debug=True)
