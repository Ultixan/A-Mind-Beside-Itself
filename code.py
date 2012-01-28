from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from constants import goals
from util import get_account
from util import template_path
from util import validate_player

import cgi
import json

class game_list(webapp.RequestHandler):
    path = template_path('index.html')

    def get(self):
        from util import get_active_games
        user = users.get_current_user()

        if not user:
            return self.redirect(
                users.create_login_url(self.request.uri)
            )
        
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
            return self.redirect(
                users.create_login_url(self.request.uri)
            )

        acc = get_account(user)
        template_values = {
            'acc': acc
        }
        self.response.out.write(
            template.render(self.path, template_values)
        )

    def post(self):
        from util import is_valid_user
        user = users.get_current_user()
        if not user:
            return self.redirect(
                users.create_login_url(self.request.uri)
            )
        
        players = [user.nickname()]
        for i in ['2','3','4']:
            player = cgi.escape(self.request.get('player' + i))
            if player and player is not '' and is_valid_user(player):
                players.append(player)

        if len(players) > 1:
            from util import create_new_game
            create_new_game(players)
            return self.redirect('/')

class populate(webapp.RequestHandler):
    def get(self):
        from util import get_world_data
        user = users.get_current_user()
        game_id = cgi.escape(self.request.get('game_id'))
        if not validate_player(user.nickname(), game_id):
            #This needs to point to a failure screen
            self.redirect('/')

        self.response.headers.add_header(
            'content-type', 
            'application/json', 
            charset='utf-8')
        self.response.out.write(
            json.dumps(get_world_data(user.nickname(), game_id))
        )

class move(webapp.RequestHandler):
    def get(self):
        from ambi import move_character
        user = users.get_current_user()
        game_id = cgi.escape(self.request.get('game_id'))
        if not validate_player(user.nickname(), game_id):
            #This needs to point to a failure screen
            self.redirect('/')
      
        x = cgi.escape(self.request.get('x'))
        y = cgi.escape(self.request.get('y'))
        
        self.response.headers.add_header(
            'content-type', 
            'application/json', 
            charset='utf-8')
        self.response.out.write(
                json.dumps(move_character(game_id, x, y))
        )

class interact(webapp.RequestHandler):
    def get(self):
        from ambi import do_interaction
        user = users.get_current_user()
        game_id = cgi.escape(self.request.get('game_id'))
        if not validate_player(user.nickname(), game_id):
            #This needs to point to a failure screen
            self.redirect('/')

        x = cgi.escape(self.request.get('x'))
        y = cgi.escape(self.request.get('y'))
        
        self.response.headers.add_header(
            'content-type', 
            'application/json', 
            charset='utf-8')
        self.response.out.write(
                json.dumps(do_interaction(game_id, x, y))
        )

urls = [
  ('/', game_list),
  ('/create', create),
  ('/populate', populate),
  ('/move', move),
  ('/interact', interact)
  ]

app = webapp.WSGIApplication(urls, debug=True)

def main():
    run_wsgi_app(app)

if __name__ == '__main__':
    main()
