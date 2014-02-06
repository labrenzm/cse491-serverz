#!/usr/bin/env python
import random
import socket
import time
import urlparse
import cgi
import jinja2
from StringIO import StringIO
from urlparse import urlparse, parse_qs



def handle_connection(conn): 
    url = conn.recv(1)
    headers = {}
    while url[-4:] != '\r\n\r\n':
        url += conn.recv(1)
    
    request, data = url.split('\r\n', 1)
    split_url = url.split()
    check_post = split_url[0]
    url_data = urlparse(split_url[1])
    path = url_data[2]
    
    for line in data.split('\r\n')[:-2]:
        k, v = line.split(': ', 1)
        headers[k.lower()] = v
    

    
    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=loader)
    first_content = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'
    
    
    if check_post == 'GET': 
        if path == '/':
            conn.send(env.get_template('index.html').render())
         
        elif path == '/content':
	    conn.send(env.get_template('content.html').render())

        elif path == '/file':
            conn.send(env.get_template('file.html').render())
       
        elif path == '/image':
            conn.send(env.get_template('image.html').render())
       
        elif path == '/form':
            conn.send(env.get_template('form.html').render())
       
        elif path == '/submit':
	    GET_form_data = parse_qs(url_data[4])
            #submit(conn, GET_form_data)
            first_name = ''.join(GET_form_data["firstname"])
            last_name = ''.join(GET_form_data["lastname"])
            vars = {'firstname':first_name, 'lastname':last_name}
            conn.send(env.get_template('submit.html').render(vars))
        else:
	   conn.send(env.get_template('404.html').render())
                
    #initializing content to be empty
    content = ''
    if check_post == 'POST':
      
        url_data_split = url.split('\r\n')
        #for i in range(1,len(url_data_split) - 2):
            #temp_header = url_data_split[i].split(': ', 1) 
            #headers[temp_header[0].lower()] = temp_header[1]
            #print temp_header
            
        while len(content) < int(headers['content-length']):
            content += conn.recv(1)
            
        #print content
            
        #Putting the POST request into an StringIO objct, fp
        fs = cgi.FieldStorage(fp=StringIO(content), headers=headers, environ={'REQUEST_METHOD' : 'POST'})
        print headers
        if path == '/submit':
            conn.send('HTTP/1.0 200 OK\r\n')
            conn.send('Content-Type: text/html\r\n\r\n')
            first_name = headers['firstname'].value
            last_name = ''.join(headers["lastname"].value)
            conn.send("Hello Mr. {first} {last}.".format(first=first_name, last=last_name))
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


