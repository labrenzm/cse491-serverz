#!/usr/bin/env python
import random
import socket
import time
from urlparse import urlparse
from StringIO import StringIO
from app import make_app

<<<<<<< HEAD

def check_path(conn, path):
    if path == '/':
        conn.send('HTTP/1.0 200 OK\r\n')
        conn.send('Content-type: text/html\r\n\r\n')
        conn.send('<h1>Hello, world.</h1>\n')
        conn.send("This is labrenzm's Web server\r\n\r\n")
        conn.send("<a href='/content'>Content</a><br />\n")
        conn.send("<a href='/file'>Files</a><br />\n")
        conn.send("<a href='/image'>Images</a><br />")
         
    elif path == '/content':
        conn.send('HTTP/1.0 200 OK\r\n')
        conn.send('Content-type: text/html\r\n\r\n')
        conn.send('<h1>You made it to the Content Page!</h1>\n')

    elif path == '/file':
        conn.send('HTTP/1.0 200 OK\r\n')
        conn.send('Content-type: text/html\r\n\r\n')
        conn.send('<h1>You made it to the Files Page!</h1>\n')

    elif path == '/image':
        conn.send('HTTP/1.0 200 OK\r\n')
        conn.send('Content-type: text/html\r\n\r\n')
        conn.send('<h1>You made it to the Images Page!</h1>\n') 




def handle_connection(conn):
    url = conn.recv(1000)  
    check_post = url.split('\r\n')[0].split(' ')[0]

    if check_post == 'GET':
        path = url.split('\r\n')[0].split(' ')[1]
        check_path(conn, path)
    if check_post == 'POST':
        conn.send('Hello World!')
    
    conn.close()







    # @comment add the \r\n for new lines
    #conn.send('HTTP/1.0 200 OK\r\n')
    #conn.send('Content-type: text/html\r\n\r\n')
    #conn.send('<h1>Hello, world.</h1>')
    #conn.send('This is labrenzm\'s Web server.')
    conn.close()


=======
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
        
    # Parse out the path and related info
    path = urlparse(req.split(' ', 3)[1])
    env['REQUEST_METHOD'] = 'GET'
    env['PATH_INFO'] = path[2]
    env['QUERY_STRING'] = path[4]
    env['CONTENT_TYPE'] = 'text/html'
    env['CONTENT_LENGTH'] = 0

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

    env['wsgi.input'] = StringIO(content)
    appl = make_app()
    result = appl(env, start_response)
    for data in result:
        conn.send(data)

    conn.close()

>>>>>>> hw6
def main():
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn() # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.
<<<<<<< HEAD
=======
    
>>>>>>> hw6

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port
<<<<<<< HEAD
        handle_connection(c)            



if __name__ == "__main__":
    main()



# Old Code, corrected is above.
# c.send('Thank you for connecting')
# c.send("""\nHTTP/1.0 200 OK
 
#  Content-Type: text/html

#  <html>
#  <head>
#  <body>
#  <h1>Hello, World!</h1>
#  this is labrenzm's web server!
#  </body>
#  </html>""")
  
#    c.send("\ngood bye.")
=======

        handle_connection(c)

if __name__ == '__main__':
   main()
>>>>>>> hw6
