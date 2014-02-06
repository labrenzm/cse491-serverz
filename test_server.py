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

def test_handle_connection_home_page():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = """<h1>Hello, world.</h1>\n
                      This is labrenzm's Web server\n
                      <br>\n
                      <a href='/content'>Content</a><br />\n
                      <a href='/file'>Files</a><br />\n
                      <a href='/image'>Images</a><br />"""
    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_content_page():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    expected_return ='<h1>You made it to the Content Page!</h1>'
    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_file_page():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    expected_return = '<h1>You made it to the Files Page!</h1>'
    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_image_page():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    expected_return = '<h1>You made it to the Images Page!</h1>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_post():
    conn = FakeConnection("POST / HTTP/1.1\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      'Hello World!'

    server.handle_connection(conn)

    print conn.sent
    print expected_return
    assert conn.sent == expected_return

def test_form():
    conn = FakeConnection("GET /submit?firstname=Matt&lastname=LaBrenz.")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n\r\n' + \
                      "Hello Mr. Matt LaBrenz."
    server.handle_connection(conn)
    assert conn.sent == expected_return, '\nExpected: %s \nGot: %s' % \
        (repr(expected_return),repr(conn.sent),)

#Test for the form when using post
def test_post_form():
    conn = FakeConnection("POST /submit HTTP/1.0\r\n\r\n firstname=Matt&lastname=LaBrenz")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                 'Content-Type: text/html\r\n\r\n' + \
                 "Hello Mr. Matt LaBrenz."
    server.handle_connection(conn)
    assert conn.sent == expected_return, '\nExpected: %s \nGot: %s' % \
        (repr(expected_return),repr(conn.sent),)
