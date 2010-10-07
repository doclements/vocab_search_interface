import web
import vocabservs


render = web.template.render('/var/www/web_services/templates', cache=False)


urls = (
    '/vservs/gemet', vocabservs.gemet,
    '/vservs/nerc', vocabservs.nerc,
    '/vservs/term', vocabservs.term,
    '/(.*)/', 'hello'
)

class hello:
    def GET(self):
        return "Hello, worldfS."

class second:
    def GET(self):
        return "Second page as simple as that"


class json:
    def GET(self):
       return "Second page as simple as that"

application = web.application(urls, globals()).wsgifunc()
