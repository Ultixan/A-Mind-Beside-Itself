import web
from google.appengine.ext import db

urls = (
  '/', 'index',
  '/note', 'note',
  '/source', 'source',
  '/crash', 'crash'
)

render = web.template.render('templates/')

class Note(db.Model):
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)

class index:
    def GET(self):
        notes = db.GqlQuery("SELECT * FROM Note ORDER BY date DESC LIMIT 10")
        return render.index(notes)

class note:
    def POST(self):
        i = web.input('content')
        note = Note()
        note.content = i.content
        note.put()
        return web.seeother('/')

class source:
    def GET(self):
        web.header('Content-Type', 'text/plain')
        return (
          '## code.py\n\n' + 
          file('code.py').read() + 
          '\n\n## templates/index.html\n\n' + 
          file('templates/index.html').read()
        )

class crash:
    def GET(self):
        import logging
        logging.error('test')
        crash

app = web.application(urls, globals())
main = app.cgirun()
