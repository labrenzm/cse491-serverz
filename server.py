#!/usr/bin/env python
import random
import socket
import urlparse

from app import make_app

def main():
    s = socket.socket() # Create a socket object.
    host = socket.getfqdn() # Get local machine name.
    port = random.randint(8000, 9999) # Assign random port.
    s.bind((host, port)) # Bind to the port.

    wsgi_app = make_app() # Creates WSGI app.

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5) # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port
        handle_connection(c, wsgi_app)
    return

def handle_connection(conn, wsgi_app):
    # Read in request until end of header sentinel.
    request = ''
    while '\r\n\r\n' not in request:
        request += conn.recv(1)

    # Avoids indexing error - makes sure there is request.
    if not request:
        conn.close()
        return

    # Creates headers dictionary.
    headers = {}
    for header in request.splitlines()[1:]:
        try:
            k, v = header.split(': ', 1)
        except:
            continue
        headers[k.lower()] = v

    # Read in rest of request to obtain message.
    message = ''
    if 'content-length' in headers:
        while len(message) < int(headers['content-length']):
            message += conn.recv(1)

    # Creates environ dictionary.
    environ = {}
    environ['REQUEST_METHOD'] = request.splitlines()[0].split(' ')[0]
    url = urlparse.urlparse(request.splitlines()[0].split(' ')[1])
    environ['PATH_INFO'] = url.path
    environ['QUERY_STRING'] = url.query
    environ['CONTENT_TYPE'] = headers.get('content-type', '')
    environ['CONTENT-LENGTH'] = headers.get('content-length', '')
    environ['wsgi.input'] = message

    # Declares variables in dictionary so they can be changed by start_response.
    # Python 2.x doesn't support nonlocal keyword.
    local = {'response' : '', 'started' : False}

    # Defines start_response function.
    def start_response(status, response_headers):
        local['started'] = True

        # Restarts response every time function is called.
        local['response'] = ''

        # Appends status line and headers.
        local['response'] += 'HTTP/1.0 {0}\r\n'.format(status)
        for header in response_headers:
            local['response'] += '{0}: {1}\r\n'.format(header[0], header[1])
        local['response'] += '\r\n' # Ends with header sentinel.

        return

    # Gets content of response from call to WSGI app.
    for response in wsgi_app(environ, start_response):
        local['response'] += response

    if local['started']:
        conn.send(local['response'])
    conn.close()
    return


if __name__ == '__main__':
    main()