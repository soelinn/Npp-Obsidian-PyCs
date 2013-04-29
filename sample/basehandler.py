import webapp2
from google.appengine.api import users
from webapp2_extras import jinja2
import gqlencoder

class BaseHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def jinja2(self):
        """
        Initializes (if not yet) and returns a cached Jinja2 instance.
        """
        # Line Comment
        # The quick brown fox jumps over the lazy dog
		# THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG
        return jinja2.Jinja2(app=self.app, config={
            'environment_args': {'trim_blocks': True},
            'globals': {
                'uri_for': webapp2.uri_for
            }
        })

    def render_response(self, template_name, **context):
        user = self.current_user()
        if user and 'CURRENT_USER_NICKNAME' not in context:
            context['CURRENT_USER_NICKNAME'] = user.nickname()
            context['LOGOUT_URL'] = users.create_logout_url('/')
        else:
            context['LOGIN_URL'] = users.create_login_url(self.request.uri)

        rv = self.jinja2.render_template(template_name, **context)
        self.response.write(rv)

    def render_json(self, o):
        self.response.content_type = 'application/json'
        self.response.charset = 'utf-8'
        return self.response.write(self.json_encode(o))

    def json_encode(self, o):
        return gqlencoder.encode(o)