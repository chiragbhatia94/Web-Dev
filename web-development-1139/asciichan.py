import os
import jinja2
import webapp2

template_dir=os.path.join(os.path.dirname(__file__),'templates')
jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                             autoescape=True)

from google.appengine.ext import db

class Handler(webapp2.RedirectHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a,**kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.response.out.write(self.render_str(template, **kw))

class Art(db.Model):
    title=db.StringProperty(required=True)
    art=db.TextProperty(required=True)
    created=db.DateTimeProperty(auto_now_add=True)

class MainPage(Handler):
    def render_front(self,title="",art="",error=""):
        arts=db.GqlQuery("select * from Art order by created desc")
        self.render("asciichan.html",error=error,title=title,art=art,arts=arts)
    def get(self):
        self.render_front()
    def post(self):
        title=self.request.get("title")
        art=self.request.get("art")
        if title and art:
            #self.write("Thanx!")
            a=Art(title=title,art=art)
            a.put()
            self.redirect("/")
        else:
            error="we need both a title and some artwork!"
            self.render_front(title,art,error)

app=webapp2.WSGIApplication([('/',MainPage)],debug=True)