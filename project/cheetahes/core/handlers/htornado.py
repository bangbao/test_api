# coding: utf-8
from tornado.web import RequestHandler


class BaseRequestHandler(RequestHandler):
    """
    """
    def summary_params(self):
        """
        """
        return self.request.arguments

    #def render_string(self, filename, **kwargs): 
    #    """Override render_string to use mako template.  
    #    """
    #    template = self._lookup.get_template(filename)
    #    env_kwargs = dict(
    #                    handler=self,
    #                    request=self.request,
    #                    current_user=self.current_user,
    #                    locale=self.locale,
    #                    _=self.locale.translate,
    #                    static_url=self.static_url,
    #                    xsrf_form_html=self.xsrf_form_html,
    #                    reverse_url=self.application.reverse_url,
    #                )
    #    env_kwargs.update(kwargs)
    #    return template.render(**env_kwargs)
    #                                                                         
    #def render(self, filename, **kwargs):
    #    self.finish(self.render_string(filename, **kwargs))

