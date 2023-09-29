import threading
import socketserver

serverMap = {}
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        cur_thread = threading.current_thread()
        print(self.client_address)
        print(cur_thread.name)
        while(True):
            global serverMap
            data = eval(self.request.recv(4096))
            if isinstance(data[0], str):
                if data[0] == 'e':
                    for i in serverMap.keys():
                        if data[1] in serverMap[i]['map']:
                            serverMap[i]['map'].remove(data[1])
                elif data[0] == 'pt':
                    serverMap[self.client_address]['pt'] = data[1]
                elif data[0] == 'join':
                    buff = {'pt':[100, 100], 'color':data[1], 'map':[]}
                    serverMap[self.client_address] = buff
                elif data[0] == 'get':
                    pass
                elif data[0] == 'end':
                    del serverMap[self.client_address]
                    break
            else:
                for i in serverMap.keys():
                    if data[1] in serverMap[i]['map']:
                        serverMap[i]['map'].remove(data[1])
                serverMap[self.client_address]['map'].append(data[1])
            buf = bytes(str(serverMap), 'utf-8')
            #print(buf)
            self.request.sendall(buf)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = '127.0.0.1', 60000
    socketserver.TCPServer.allow_reuse_address = True
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    #with server:
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    #server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)
    #server.serve_forever()