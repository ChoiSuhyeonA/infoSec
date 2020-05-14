import cherrypy
import string
from caesarCipherCore import encrypt, decrypt

LETTERS = string.ascii_uppercase + string.ascii_letters + string.whitespace

class GetMessage(object):

    @cherrypy.expose()
    def index(self):
        html_body = \
        """
            <html>
            <body>
            <p>
            <form method ="get" action="get_msg">
                <input type="text" value="" name="input_msg" />
                <input type="text" value="" name="key" />
                <button type="submit">Click!</button>
            </form>
            </body>
            </html>
            """
        return html_body

    @cherrypy.expose
    def function(self):
        # 내용 작성 후에 아래 내용을 추가
        html_shutdown = "<a id='shutdown'; href='./shutdown'>Shutdown Server</a>"
        return html_shutdown

    @cherrypy.expose
    def shutdown(self):
        cherrypy.engine.exit()

    @cherrypy.expose()
    def get_msg(self, input_msg,key):
        return "Cipher Text %s!" % encrypt(input_msg,int(key),LETTERS)


if __name__ == '__main__':
    cherrypy.config.update({'server.socket_port': 8081})
    cherrypy.quickstart(GetMessage())