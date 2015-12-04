import os
import jinja2
import webapp2

template_dir=os.path.join(os.path.dirname(__file__),'templates')
jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                             autoescape=True)

from google.appengine.ext import db

class Blog(db.Model):
    subject=db.StringProperty(required=True)
    content=db.TextProperty(required=True)
    created=db.DateTimeProperty(auto_now_add=True)

class Handler(webapp2.RedirectHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a,**kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.response.out.write(self.render_str(template, **kw))

class MainPage(Handler):
    def render_front(self):
        blogs=db.GqlQuery("select * from Blog order by created desc limit 10")
        self.render("blog.html",blogs=blogs)
    def get(self):
        self.render_front()

class NewPostHandler(Handler):
    def render_front(self,subject="",content="",error=""):
        self.render("newpost.html",error=error,subject=subject,content=content)
    def get(self):
        self.render("newpost.html")
    def post(self):
        subject=self.request.get("subject")
        content=self.request.get("content")
        if subject and content:
            blog=Blog(subject=subject,content=content)
            blog.put()
            id=blog.key().id()
            self.redirect('/'+str(id))

        else:
            error="we need both a subject and content!"
            self.render_front(subject,content,error)
        #self.render_front()

app=webapp2.WSGIApplication([('/blog',MainPage),('/newpost',NewPostHandler)],debug=True)