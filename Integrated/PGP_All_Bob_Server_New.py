import os

import cherrypy
from cherrypy.lib import static

from Integrated.PGP_All_Common import *

localDir = os.path.dirname(__file__)
absDir = os.path.join(os.getcwd(), localDir)

class App():


    bob_publickey = './HybridBob/bobpublickey.txt'

    """
    PGP_Generate_Key_File(bob_privatekey, bob_publickey)
    PGP_Client_Receive_File('localhost', 6000, alice_publickey)
    PGP_Server_Send_File('localhost', 7000, bob_publickey)
    """

    def dec(self, upload_filename):
        received_data_base64 = open(upload_filename, "rb").read()
        bob_privatekey = './HybridBob/bobprivatekey.txt'
        #bob_received_output_b64 = './HybridBob/received_outputAlice_b64.txt'
        #PGP_Client_Receive_File('localhost', 8008, bob_received_output_b64)

        bob_received_output = './HybridBob/received_outputAlice.txt'

        B64Decoding(received_data_base64, bob_received_output)

        bob_received_sig_MSG_alice = './HybridBob/sig_MSG_Alice.txt'
        dec_output = Generate_AES_Dec_For_DigSig_Plus_Key(bob_received_output, bob_privatekey, bob_received_sig_MSG_alice)
        return dec_output
    def verify(self):
        alice_publickey = './HybridBob/received_alicepublickey.txt'
        bob_received_sig_MSG_alice = './HybridBob/sig_MSG_Alice.txt'
        Verify_DigSig_On_Hashed_File(bob_received_sig_MSG_alice, alice_publickey)


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


    @cherrypy.expose
    def upload(self, myFile):
        # Either save the file to the directory where server.py is
        # or save the file to a given path:
        # upload_path = '/path/to/project/data/'
        upload_path = os.path.dirname(__file__)

        # Save the file to a predefined filename
        # or use the filename sent by the client:
        # upload_filename = ufile.filename
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
                size += len(data)
        out.close()
        decrypted_message = self.dec(upload_file)
        out = '''
            <html>
            <p>File received.

            <p>received data: {}
            <p>decrypted data: {}
            </html>
            '''.format(data, decrypted_message)
        return out


    @cherrypy.expose
    def download(self):
        path = os.path.join(absDir, './HybridBob/bobpublickey.txt')
        return static.serve_file(path, 'application/x-download', 'attachment', os.path.basename(path))

if __name__ == '__main__':


    cherrypy.quickstart(App())