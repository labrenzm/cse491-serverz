#!/usr/bin/env python
import random
import socket
import time
import urlparse
import cgi
import StringIO
import jinja2

def main():
    s = socket.socket()	# Create a socket object
    host = socket.getfqdn()	# Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))	# Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)

    # Now wait for client connection.
    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port
        handle_connection(c)
    return

def handle_connection(conn):
    request = ''
    while '\r\n\r\n' not in request:
        request += conn.recv(1)

    if not request: # Avoids indexing error.
        conn.close()
        return

    method = request.splitlines()[0].split(' ')[0]
    url = urlparse.urlparse(request.splitlines()[0].split(' ')[1])

    # Send intial line and headers.
    initResp = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'

    # Sets up jinja2.
    loader = jinja2.FileSystemLoader('./templates')
    jenv = jinja2.Environment(loader=loader)

    # Send the appropriate payload.
    if method == 'POST':
        conn.send(initResp)
        headers, message = get_headers_and_message(conn, request)

        if url.path == '/submit-post-app':
            # With this enctype, message is treated same as GET.
            handle_submit(conn, message, jenv)
        elif url.path == '/submit-post-multi':
            handle_submit_multi(conn, headers, message, jenv)
        else:
            handle_post(conn, jenv)
    elif url.path == '/':
        conn.send(initResp)
        handle_default(conn, jenv)
    elif url.path == '/content':
        conn.send(initResp)
        handle_content(conn, jenv)
    elif url.path == '/file':
        conn.send(initResp)
        handle_file(conn, jenv)
    elif url.path == '/image':
        conn.send(initResp)
        handle_image(conn, jenv)
    elif url.path == '/form-get':
        conn.send(initResp)
        handle_form_get(conn, jenv)
    elif url.path == '/form-post-app':
        conn.send(initResp)
        handle_form_post_app(conn, jenv)
    elif url.path == '/form-post-multi':
        conn.send(initResp)
        handle_form_post_multi(conn, jenv)
    elif url.path == '/submit-get':
        conn.send(initResp)
        handle_submit(conn, url.query, jenv)
    else:
        conn.send('HTTP/1.0 404 Not Found\r\n\r\n')
        conn.send(jenv.get_template('404.html').render())

    conn.close()
    return

def handle_default(conn, jenv):
    conn.send(jenv.get_template('Default.html').render())
    return

def handle_content(conn, jenv):
    conn.send(jenv.get_template('Content.html').render())
    return

def handle_file(conn, jenv):
    conn.send(jenv.get_template('File.html').render())
    return

def handle_image(conn, jenv):
    conn.send(jenv.get_template('Image.html').render())
    return

def handle_post(conn, jenv):
    conn.send(jenv.get_template('PostDefault.html').render())
    return

def handle_form_get(conn, jenv):
    conn.send(jenv.get_template('FormGet.html').render())
    return

def handle_form_post_app(conn, jenv):
    conn.send(jenv.get_template('FormPostApp.html').render())
    return

def handle_form_post_multi(conn, jenv):
    conn.send(jenv.get_template('FormPostMulti.html').render())
    return

def handle_submit(conn, query, jenv):
    queryDict = urlparse.parse_qs(query)
    vars = dict(firstname=queryDict['firstname'][0],
                lastname=queryDict['lastname'][0])

    conn.send(jenv.get_template('Submit.html').render(vars))
    return

def handle_submit_multi(conn, headers, message, jenv):
    # Creates POST content string.
    content = StringIO.StringIO(message)

    # Creates environment dictionary.
    env = {'REQUEST_METHOD':'POST'}

    # Creates Field Storage object that contains values for form fields.
    form = cgi.FieldStorage(fp=content, headers=headers, environ=env)

    vars = dict(firstname=form.getvalue('firstname'),
                lastname=form.getvalue('lastname'))
    conn.send(jenv.get_template('Submit.html').render(vars))

    content.close() # Closes StringIO object.
    return

def get_headers_and_message(conn, request):
    # Creates headers dictionary.
    headersDict = {}
    headers = request.splitlines()[1:] # Gets header lines.
    for header in headers:
        try:
            k, v = header.split(': ', 1)
        except:
            continue
        headersDict[k.lower()] = v

    # Extracts message from request.
    message = ''
    while len(message) < int(headersDict['content-length']):
        message += conn.recv(1)

    return headersDict, message


if __name__ == '__main__':
    main()
