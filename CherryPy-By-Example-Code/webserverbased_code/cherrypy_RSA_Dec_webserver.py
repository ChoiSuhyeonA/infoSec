import os
import os.path

import cherrypy
from cherrypy.lib import static
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
from pyparsing import unicode

localDir = os.path.dirname(__file__)
absDir = os.path.join(os.getcwd(), localDir)

class FileDemo(object):

    @cherrypy.expose
    def index(self):
        return """
        <html><body>
            <h2>Upload a file</h2>
            <form action = "upload" method = "post" enctype = "multipart/form-data">
            filename: <input type = "file" name = "myFile" /><br/>
            <input type = "submit" />
            </form>
            <h2>Download a file</h2>
            <a href = 'download'>Public Key of Web Server</a>
        </body></html>
        """
    def RSA_Decrypt(self, upload_filename):
        received_data_base64 = open(upload_filename, "rb").read()
        recipient_private_key = RSA.import_key(open("private_WebServer.bin").read())
        print("Web Server's Private_Key: ", recipient_private_key.export_key())
        received_data = base64.b32decode(received_data_base64)
        cipher_rsa = PKCS1_OAEP.new(recipient_private_key)
        decrypted_message = cipher_rsa.decrypt(received_data)
        print("Web Server가 수신한 메시지: ", decrypted_message.decode())
        return decrypted_message.decode()

    @cherrypy.expose
    def upload(self, myFile):
        # 전송하고자 하는 파일을 선택하는 부분
        # --> 본 파일이 위치한 폴더 위치를 지정하거나 또는 임의의 폴더를 선택하도록 설정할 수 있다.
        # upload_path = '/path/to/project/data/'
        upload_path = os.path.dirname(__file__) #임의의 폴더를 선택 할 수 있도록 한다.

        # 업로드된 파일을 저장하고자 하는 파일명
        #'saved.bin'으로 저장하도록 지정함
        # 만일 업로드된 파일 이름명 그대로 저장하고자 할 경우에는 아래와 같이 설정
        # upload_filename = myFile.filename
        upload_filename = 'saved.bin'

        upload_file = os.path.normpath(os.path.join(upload_path, upload_filename))
        size = 0

        html_out_text = ""

        with open(upload_file, 'wb') as out:
            while True:
                data = myFile.file.read(8192)
                if not data:
                    break
                out.write(data)
                html_out_text += unicode(data)
                print(data)
                size += len(data)
        out.close()

        decrypted_message = self.RSA_Decrypt(upload_file)

        webpage_output = """
                <html>
                <h1>OK. Received File...</h1>
                <p>Let's Decrypt File Using Web Server's Private Key for RSA
                <p>Filename: {}
                <p>Length: {}
                <p>Received Data: {}
                <p>
                <p>
                <p>Decrypted Data: {}
                </html>
                """.format(myFile.filename, size, myFile.content_type, html_out_text)
        # 결과를 리턴 ---> 화면에 HTML 코드로 출력함
        return webpage_output

    @cherrypy.expose
    def download(self):
        path = os.path.join(absDir, 'public_WebServer.bin')
        return static.serve_file(path, 'application/x-download', 'attachment', os.path.basename(path))

#tutconf = os.path.join(os.path.dirname(__file__), 'tutorial.conf')

if __name__ == '__main__':
    # 실행순서 (및 로직)
    # 서버: cherrypy_RSA_KeyGen_And_Dec_WebServer.py 실행
    # 서버: Web Server의 Public_Key/ Private_Key 파일을 각각 생성함
    # 서버: http://127.0.0.1:8080 부분 클릭해서 웹서버 실행
    # 클라이언트: 웹 페이지에서 Public_Key 파일 다운로드 받음
    # 클라이언트: 다운받은 Public_Key를 폴더에 복사해 놓음
    # 클라이언트: cherrypy_RSA_KeyDownload_And_Enc_Client.py 실행 ---> encrypted_data_from_Alice 파일이 만들어짐
    # 클라이언트: 웹 페이지에 encrypted_data_from_Alice.bin 파일을 업로드함.
    # 서버: 업로드된 파일에 대해 복호화 과정을 자동으로 수행하고 복호화 결과를 화면에 표시함

    # Web Server(Bob)의 공개키/개인키는 한번 만 생성하면 됨..
    key = RSA.generate(2048)
    private_key = key.export_key()    #Web Server의 Private_Key
    file_out = open("private_WebServer.bin", "wb")
    file_out.write(private_key)
    file_out.close()

    public_key = key.publickey().export_key()       #Web Server의 Public_Key
    file_out = open("public_WebServer.bin", "wb")
    file_out.write(public_key)
    file_out.close()

    cherrypy.quickstart(FileDemo())