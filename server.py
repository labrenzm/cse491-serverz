import time
import socket
import random
from urlparse import urlparse
from wsgiref.validate import validator
from StringIO import StringIO
import imageapp

# from wsgiref.validate import validator
import quixote
#from quixote.demo import create_publisher
#from quixote.demo.mini_demo import create_publisher
#from quixote.demo.altdemo import create_publisher


imageapp.setup()
p = imageapp.create_publisher()
_the_app = None
def make_app():
    global _the_app

    if _the_app is None:
        _the_app = quixote.get_wsgi_app()

    return _the_app
  
def handle_connection(conn):
    # Start reading in data from the connection
    req = conn.recv(1)
    count = 0
    env = {}
    while req[-4:] != '\r\n\r\n':
        req += conn.recv(1)
  
    # Parse the headers we've received
    req, data = req.split('\r\n',1)
    headers = {}
    for line in data.split('\r\n')[:-2]:
        k, v = line.split(': ', 1)
        headers[k.lower()] = v
          
          
    env['wsgi.multithread']  = False
    env['wsgi.multiprocess'] = False
    env['wsgi.run_once']     = False
    env['wsgi.url_scheme'] = 'http'
    # Parse out the path and related info
    path = urlparse(req.split(' ', 3)[1])
    env['REQUEST_METHOD'] = 'GET'
    env['PATH_INFO'] = path[2]
    env['QUERY_STRING'] = path[4]
    env['CONTENT_TYPE'] = 'text/html'
    env['CONTENT_LENGTH'] = 0
    env['SERVER_NAME'] = 'arctic.cse.msu.edu'
    env['SCRIPT_NAME'] = ''

    def start_response(status, response_headers):
        conn.send('HTTP/1.0 ')
        conn.send(status)
        conn.send('\r\n')
        for pair in response_headers:
            key, header = pair
            conn.send(key + ': ' + header + '\r\n')
        conn.send('\r\n')

    content = ''
    if req.startswith('POST '):
        env['REQUEST_METHOD'] = 'POST'
        env['CONTENT_LENGTH'] = headers['content-length']
        env['CONTENT_TYPE'] = headers['content-type']
        print headers['content-length']

        while len(content) < int(headers['content-length']):
            content += conn.recv(1)
    env['HTTP_COOKIE'] = headers['cookie'] if 'cookie' in headers.keys() else ''
    env['wsgi.input'] = StringIO(content)
    appl = make_app()
    result = appl(env, start_response)
    for data in result:
        conn.send(data)

    conn.close()

def main():
  
    
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn() # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))        # Bind to the port
    
    # validate_app = validator(wsgi_app)
    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.
    

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port

        handle_connection(c)


if __name__ == '__main__':
   main()