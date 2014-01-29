#!/usr/bin/env python
import random
import socket
import time
from urlparse import urlparse, parse_qs

def index(conn, path, variables):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n\r\n')
    conn.send('<h1>Hello, world.</h1>\n')
    conn.send("This is labrenzm's Web server\r\n\r\n")
    conn.send("<a href='/content'>Content</a><br />\n")
    conn.send("<a href='/file'>Files</a><br />\n")
    conn.send("<a href='/image'>Images</a><br />")   

def content(conn, path, variables):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n\r\n')
    conn.send('<h1>You made it to the Content Page!</h1>\n')

def file(conn, path, variables):
     conn.send('HTTP/1.0 200 OK\r\n')
     conn.send('Content-type: text/html\r\n\r\n')
     conn.send('<h1>You made it to the Files Page!</h1>\n')

def image(conn, path, variables):
     conn.send('HTTP/1.0 200 OK\r\n')
     conn.send('Content-type: text/html\r\n\r\n')
     conn.send('<h1>You made it to the Images Page!</h1>\n')

def form(conn, path, variables):
      conn.send('HTTP/1.0 200 OK\r\n')
      conn.send('Content-type: text/html\r\n\r\n')
      conn.send("<form action='/submit' method='GET'>")
      conn.send("<input type='text' name='firstname'>")
      conn.send("<input type='text' name='lastname'>") 
      conn.send("<button type='submit'>Submit</button>")
      conn.send('</form>')

def submit(conn, path, variables):
      conn.send('HTTP/1.0 200 OK\r\n')
      conn.send('Content-type: text/html\r\n\r\n')
      conn.send("Hello Mr. %s %s" % (variables.get('firstname')[0], \
          variables.get('lastname')[0]))

def check_path(conn, path, variables):
    if path == '/':
        index(conn, path, variables) 
         
    elif path == '/content':
        content(conn, path, variables) 

    elif path == '/file':
        file(conn, path, variables)
       
    elif path == '/image':
        image(conn, path, variables)
       
    elif path == '/form':
        form(conn, path, variables)
       
    elif path == '/submit':
        submit(conn, path, variables)



def handle_connection(conn):
    url = conn.recv(1000).splitlines()  
    check_post = url[0].split(' ')[0]
    request = urlparse(url[0].split(' ')[1])
    path = request[2] 
    if check_post == 'GET': 
        variables = parse_qs(request[4])
        check_path(conn, path, variables)
    if check_post == 'POST':
        if path == '/submit':
            post_variables = conn.recv(1000).split('&')
            firstname = post_variables[0].split('=')[1]
            lastname = post_variables[1].split('=')[1]
            conn.send('HTTP/1.0 200 OK\r\n')
            conn.send('Content-type: application/x-www-form-urlencoded\r\n\r\n')
            conn.send("Hello %s %s" % (firstname, lastname))
        else:
            conn.send('HTTP/1.0 200 OK\r\n')
            conn.send('Content-type: text/html\r\n\r\n')
            conn.send('Hello World!')
    
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


