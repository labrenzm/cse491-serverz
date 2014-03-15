import server

from app import make_app

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
    app = make_app()
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<html>\n    <body>\n        \n<title>Home</title>\n' + \
                      '<h1>Welcome to john3209\'s Web Server!</h1>\n<a hre' + \
                      'f="/content">Content</a><br />\n<a href="/file">Fil' + \
                      'e</a><br />\n<a href="/image">Image</a><br />\n<a h' + \
                      'ref="/form-get">Form (Get)</a><br />\n<a href="/for' + \
                      'm-post-app">Form (Post-App)</a><br />\n<a href="/fo' + \
                      'rm-post-multi">Form (Post-Multi)</a>\n\n    </body>' + \
                      '\n</html>'

    server.handle_connection(conn, app)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    app = make_app()
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<html>\n    <body>\n        \n<title>Content</title' + \
                      '>\n<h1>This is john3209\'s content!</h1>\n\n    </b' + \
                      'ody>\n</html>'

    server.handle_connection(conn, app)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    app = make_app()
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/plain\r\n\r\n' + \
                      'Test file!'

    server.handle_connection(conn, app)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    app = make_app()
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: image/jpeg\r\n\r\n'

    server.handle_connection(conn, app)

    assert conn.sent.startswith(expected_return), 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_post():
    fakeRequest = "POST / HTTP/1.0\r\n" + \
                  "Content-Length: 0\r\n\r\n"

    conn = FakeConnection(fakeRequest)
    app = make_app()
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<html>\n    <body>\n        \n<title>Post</title>\n' + \
                      '<h1>Hello World!</h1>\n\n    </body>\n</html>'

    server.handle_connection(conn, app)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_form_get():
    conn = FakeConnection("GET /form-get HTTP/1.0\r\n\r\n")
    app = make_app()
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<html>\n    <body>\n        \n<title>Form (Get)</ti' + \
                      'tle>\n<form action=\'/submit-get\' method=\'GET\'>\n' + \
                      '    First Name: <input type=\'text\' name=\'firstname\'' + \
                      '><br>\n    Last Name: <input type=\'text\' name=\'l' + \
                      'astname\'><br>\n    <input type=\'submit\' value=\'' + \
                      'Submit\'>\n</form>\n\n    </body>\n</html>'

    server.handle_connection(conn, app)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_form_post_app():
    conn = FakeConnection("GET /form-post-app HTTP/1.0\r\n\r\n")
    app = make_app()
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<html>\n    <body>\n        \n<title>Form (Post-App' + \
                      ')</title>\n<form action=\'/submit-post-app\' method' + \
                      '=\'POST\' enctype=\'application/x-www-form-urlencod' + \
                      'ed\'>\n    First Name: <input type=\'text\' name=\'' + \
                      'firstname\'><br>\n    Last Name: <input type=\'text\'' + \
                      ' name=\'lastname\'><br>\n    <input type=\'submit\' ' + \
                      'value=\'Submit\'>\n</form>\n\n    </body>\n</html>'

    server.handle_connection(conn, app)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_form_post_multi():
    conn = FakeConnection("GET /form-post-multi HTTP/1.0\r\n\r\n")
    app = make_app()
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<html>\n    <body>\n        \n<title>Form (Post-Mul' + \
                      'ti)</title>\n<form action=\'/submit-post-multi\' me' + \
                      'thod=\'POST\' enctype=\'multipart/form-data\'>\n   ' + \
                      ' First Name: <input type=\'text\' name=\'firstname\'' + \
                      '><br>\n    Last Name: <input type=\'text\' name=\'l' + \
                      'astname\'><br>\n    <input type=\'submit\' value=\'' + \
                      'Submit\'>\n</form>\n\n    </body>\n</html>'

    server.handle_connection(conn, app)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_submit_get():
    conn = FakeConnection("GET /submit-get?firstname=Jeff&lastname=Johnson HTTP/1.0\r\n\r\n")
    app = make_app()
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<html>\n    <body>\n        \n<title>Hello!</title>' + \
                      '\n<h1>Hello Mr. Jeff Johnson.</h1>\n\n    </body>\n' + \
                      '</html>'

    server.handle_connection(conn, app)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_submit_post_app():
    fakeRequest = "POST /submit-post-app HTTP/1.0\r\n" + \
                  "Content-Type: application/x-www-form-urlencoded\r\n" + \
                  "Content-Length: 31\r\n\r\n" + \
                  "firstname=Jeff&lastname=Johnson"

    conn = FakeConnection(fakeRequest)
    app = make_app()
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      '<html>\n    <body>\n        \n<title>Hello!</title>' + \
                      '\n<h1>Hello Mr. Jeff Johnson.</h1>\n\n    </body>\n' + \
                      '</html>'

    server.handle_connection(conn, app)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)