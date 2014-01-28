#!/usr/bin/env python
import random
import socket
import time


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
    elif path == '/form':
        conn.send('HTTP/1.0 200 OK\r\n')
        conn.send('Content-type: text/html\r\n\r\n')
        conn.send("<form action='/submit' method='GET'>")
        conn.send("<input type='text' name='firstname'>")
        conn.send("<input type='text' name='lastname'>") 
        conn.send("<button type='submit'>Submit</button>")
        conn.send('</form>')



def handle_connection(conn):
    url = conn.recv(1000)  
    check_post = url.split('\r\n')[0].split(' ')[0]

    if check_post == 'GET':
        path = url.split('\r\n')[0].split(' ')[1]
        check_path(conn, path)
    if check_post == 'POST':
        conn.send('HTTP/1.0 200 OK\r\n')
        conn.send('Content-type: text/html\r\n\r\n')
        conn.send('Hello World!')
    
    conn.close()







    # @comment add the \r\n for new lines
    #conn.send('HTTP/1.0 200 OK\r\n')
    #conn.send('Content-type: text/html\r\n\r\n')
    #conn.send('<h1>Hello, world.</h1>')
    #conn.send('This is labrenzm\'s Web server.')
    conn.close()


def main():
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn() # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port
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
