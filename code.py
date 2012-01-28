from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from constants import goals
from django.utils import simplejson as json

class Game(db.Model):
    game_id = db.StringProperty()
    players = db.StringListProperty()
    current_player = db.IntegerProperty()
    goals = db.IntegerProperty()
    content = db.ListProperty(int)
    move_counter = db.IntegerProperty()

class Player(db.Model):
    game_id = db.StringProperty()
    x = db.IntegerProperty()
    y = db.IntegerProperty()

class Account(db.Model):
    user = db.UserProperty()
    games = db.StringListProperty()

class usertest(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.response.headers['Content-Type'] = 'text/plain'
            existing = db.GqlQuery('SELECT * from Account ' +
                'WHERE user = :1',
                user)
            if existing.count() == 0:
                account = Account()
                account.user = user
                account.put()
                self.response.out.write('Hello, ' + user.nickname())
            else:
                acc = existing[0]
                self.response.out.write(acc.user.nickname())
        else:
            self.redirect(users.create_login_url(self.request.uri))

urls = [
  ('/', usertest)
  ]

app = webapp.WSGIApplication(urls)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
