from socket import socket
from struct import unpack
#import ssl



class GET_sock(socket):
    def __init__(self, family = 2,type = 1):#socket.AF_INET socket.SOCK_STREAM
        super().__init__(family, type)



class MainCLI(GET_sock):
    #def __init__(self):

    def main(self):
        server_address = ('127.0.0.1',5555)
        #self.bind(('127.0.0.1', 5555))

        #self.listen(1)


        #context = ssl.create_default_context()

        # Wrap the socket with SSL
        #ssl_sock = context.wrap_socket(self, server_hostname='22:22:22:22')
        try:
            # Connect to the server
            self.connect(server_address)
            
            # Message to send
            message = b'Hello, secure server!'
            while True:
                self.send(message)
                print('OKK')
        except Exception as i:
            print(i)

MainCLI().main()
