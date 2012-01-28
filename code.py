from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from constants import goals
from util import get_account
from util import template_path

import cgi

class usertest(webapp.RequestHandler):
    path = template_path('index.html')

    def get(self):
        from util import get_active_games
        import json
        from util import create_world_data
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
 
#        self.response.out.write(json.dumps(create_world_data()))
        acc = get_account(user)
        games = get_active_games(user)
        template_values = {
            'acc': acc,
            'games': games
        }
        self.response.out.write(
            template.render(self.path, template_values)
        )

class create(webapp.RequestHandler):
    path = template_path('create.html')

    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))

        acc = get_account(user)
        template_values = {
            'acc': acc
        }
        self.response.out.write(
            template.render(self.path, template_values)
        )

    def post(self):
        from util import get_valid_account
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
        
        players = [user.nickname()]
        self.response.out.write('<html><body>')
        for i in ['2','3','4']:
            player = cgi.escape(self.request.get('player' + i))
            if player and player is not '' and is_valid_user(player):
                players.append(player)

        if len(players) > 1:
            from util import create_new_game
            create_new_game(players)

urls = [
  ('/', usertest),
  ('/create', create)
  ]

app = webapp.WSGIApplication(urls, debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
