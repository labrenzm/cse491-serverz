import server

class FakeConnection(object):
    """
    A fake connection class that mimics a real TCP socket for the purpose
    of testing socket I/O.
    """
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r
            
        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s

    def close(self):
        self.is_closed = True

# Test a basic GET call.

def test_handle_connection_default():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<html><body>' + \
                      '<h1>Welcome to john3209\'s Web Server!</h1>' + \
                      '<a href="/content">Content</a><br />' + \
                      '<a href="/file">File</a><br />' + \
                      '<a href="/image">Image</a><br />' + \
                      '<a href="/form-get">Form (Get)</a><br />' + \
                      '<a href="/form-post-app">Form (Post-App)</a><br />' + \
                      '<a href="/form-post-multi">Form (Post-Multi)</a>' + \
                      '</body></html>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<html><body>' + \
                      '<h1>This is john3209\'s content!</h1>' + \
                      '</body></html>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<html><body>' + \
                      '<h1>This is john3209\'s file!</h1>' + \
                      '</body></html>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<html><body>' + \
                      '<h1>This is john3209\'s image!</h1>' + \
                      '</body></html>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_post():
    fakeRequest = "POST / HTTP/1.0\r\n" + \
                  "Content-Length: 0\r\n\r\n"

    conn = FakeConnection(fakeRequest)
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<html><body>' + \
                      '<h1>Hello World!</h1>' + \
                      '</body></html>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_form_get():
    conn = FakeConnection("GET /form-get HTTP/1.0\r\n\r\n")
    expected_return = "HTTP/1.0 200 OK\r\n" + \
                      "Content-type: text/html\r\n" + \
                      "\r\n" + \
                      "<html><body>" + \
                      "<form action='/submit-get' method='GET'>" + \
                      "First Name: <input type='text' name='firstname'><br>" + \
                      "Last Name: <input type='text' name='lastname'><br>" + \
                      "<input type='submit' value='Submit'>" + \
                      "</form></body></html>"

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_form_post_app():
    conn = FakeConnection("GET /form-post-app HTTP/1.0\r\n\r\n")
    expected_return = "HTTP/1.0 200 OK\r\n" + \
                      "Content-type: text/html\r\n" + \
                      "\r\n" + \
                      "<html><body>" + \
                      "<form action='/submit-post-app' method='POST' " + \
                      "enctype='application/x-www-form-urlencoded'>" + \
                      "First Name: <input type='text' name='firstname'><br>" + \
                      "Last Name: <input type='text' name='lastname'><br>" + \
                      "<input type='submit' value='Submit'>" + \
                      "</form></body></html>"

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_form_post_multi():
    conn = FakeConnection("GET /form-post-multi HTTP/1.0\r\n\r\n")
    expected_return = "HTTP/1.0 200 OK\r\n" + \
                      "Content-type: text/html\r\n" + \
                      "\r\n" + \
                      "<html><body>" + \
                      "<form action='/submit-post-multi' method='POST' " + \
                      "enctype='multipart/form-data'>" + \
                      "First Name: <input type='text' name='firstname'><br>" + \
                      "Last Name: <input type='text' name='lastname'><br>" + \
                      "<input type='submit' value='Submit'>" + \
                      "</form></body></html>"

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_submit_get():
    conn = FakeConnection("GET /submit-get?firstname=Jeff&lastname=Johnson HTTP/1.0\r\n\r\n")
    expected_return = "HTTP/1.0 200 OK\r\n" + \
                      "Content-type: text/html\r\n" + \
                      "\r\n" + \
                      "<html><body>" + \
                      "<h1>Hello Mr. Jeff Johnson.</h1>" + \
                      "</body></html>"

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_submit_post_app():
    fakeRequest = "POST /submit-post-app HTTP/1.0\r\n" + \
                  "Content-Type: application/x-www-form-urlencoded\r\n" + \
                  "Content-Length: 31\r\n\r\n" + \
                  "firstname=Jeff&lastname=Johnson"

    conn = FakeConnection(fakeRequest)
    expected_return = "HTTP/1.0 200 OK\r\n" + \
                      "Content-type: text/html\r\n" + \
                      "\r\n" + \
                      "<html><body>" + \
                      "<h1>Hello Mr. Jeff Johnson.</h1>" + \
                      "</body></html>"

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

