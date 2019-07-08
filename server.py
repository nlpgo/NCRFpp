import sys
import socket
from pprint import pprint
from contextlib import closing

class Server(object):
    def __init__(self, port, data, function):
        self.port = int(port)
        self.data = data
        self.function = function
    
    def run(self):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            print 'Starting server in port %d' % self.port
            s.bind(('127.0.0.1', self.port))
            sys.stdout.flush()
            s.listen(1)
            while True:
                conn, addr = s.accept()
                print 'Connection from: ', addr 
                config_path = conn.recv(1024)
                self.data.read_config(config_path) # Reload config to update input and output directories
                self.data.generate_instance('raw')
                try:
                    print 'Try decode...'
                    sys.stdout.flush()
                    self.function(self.data)
                    conn.sendall('ok')
                except Exception as e:
                    print e.message
                    conn.sendall(str(e))


