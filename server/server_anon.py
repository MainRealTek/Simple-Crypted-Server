import asyncio
from concurrent.futures import ThreadPoolExecutor
#from ssl import SSLContext,PROTOCOL_TLS_SERVER,create_default_context,Purpose,wrap_socket
from sniffsafe import MainServerSNIFF
from socket import socket,AF_INET,SOCK_STREAM#SOL_SOCKET,SO_REUSEADDR


class GET_sock(socket):
    def __init__(self, family = AF_INET,type = SOCK_STREAM):
        super().__init__(family, type)

class MainServerREQ(GET_sock):
    def main(self):
        self.bind(('127.0.0.1', 5555))
        self.listen()

        while True:
            connection, client_address = self.accept()
            while True:
                data = connection.recv(1024)
                print(connection,client_address,data)
                if not data:
                    break
                print(f"Received: {data.decode('utf-8')}")

        #client_socket.close()
        #secure_socket.close()




class MainPROTO(object):
    def __init__(self):
        self.coros = [MainServerREQ(),MainServerSNIFF()]
        self.executor_thrds   = ThreadPoolExecutor(max_workers=2)
        super().__init__(self.run())

    def wrapper(self,coro):
        return asyncio.run(coro.main())

    def run(self):
        for r in self.executor_thrds.map(self.wrapper, self.coros):
            print(r)


MainPROTO()



