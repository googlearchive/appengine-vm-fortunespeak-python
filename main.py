import webapp2

class HelloHandler(webapp2.RequestHandler):
  def get(self):
    msg = 'hello %s\n' % self.request.headers.get('X-AppEngine-Country', 'world')
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write(msg)

app = webapp2.WSGIApplication([('/', HelloHandler)],
                               debug=True)
