import cherrypy, random, string

LETTERS = string.ascii_lowercase
def encrypt(message,key,LETTERS):
    encrypt_message=''
    for symbol in message:
        if symbol in LETTERS:
            num = ( LETTERS.find(symbol) + key ) % (len(LETTERS))
            encrypt = LETTERS[num]
        else:
            encrypt = symbol
        encrypt_message = encrypt_message + encrypt
    return encrypt_message

def decrypt(encrypt_message,key,LETTERS):
    decrypt_message=''
    for symbol in encrypt_message:
        if symbol in LETTERS:
            num = ( LETTERS.find(symbol) - key ) % (len(LETTERS))
            decrypt = LETTERS[num]
        else:
            decrypt = symbol
        decrypt_message = decrypt_message + decrypt
    return decrypt_message

class HelloWorld(object):

    @cherrypy.expose
    def index(self):
        return """
                <html>
                <head><title>About Us</title></head>
                <body>
                <h1>About Us</h1>
                <p1> 체리파이를 이용한 홈페이지</p1>
                <p>
                <form method="get" action="get_encrypt">
               
                  <input type="text" value="Enter msg" name="get_name"/>
                  <input type="text" value="Enter key" name="get_key"/>
                  <button type="submit">GET encrypt!</button>
                </form>
                </p>
                <p>
                <form method="get" action="get_decrypt">
                
                  <input type="text" value="Enter msg" name="get_name"/>
                  <input type="text" value="Enter key" name="get_key"/>
                  <button type="submit">GET decrypt!</button>
                </form>
                </p>
                </body>
                </html>
                """

    # form method = "get"은
    #     URL로
    #     정보전달.post는
    #     용량이
    #     큰
    #     파일
    #     전송에서
    #     숨겨진
    #     상태로
    #     보여진다.


    def function(self):
        # 내용 작성 후에 아래 내용을 추가
        html_shutdown = "<a id='shutdown'; href='./shutdown'>Shutdown Server</a>"
        return html_shutdown

    @cherrypy.expose
    def shutdown(self):
        cherrypy.engine.exit()

    @cherrypy.expose()
    def genearte(self):
        return ''.join(random.sample(string.hexdigits,8))

    @cherrypy.expose()
    def get_encrypt(self, get_name, get_key):
        return "Result = %s" % encrypt(get_name, int(get_key), LETTERS)

    @cherrypy.expose()
    def get_decrypt(self, get_name, get_key):
        return "Result = %s"% decrypt(get_name, int(get_key), LETTERS)



cherrypy.quickstart(HelloWorld())
cherrypy.config.update({'server.socket_port':8081})