
#!/usr/bin/env python
import socket
import urlparse
import cgi
import StringIO
import jinja2

def make_app():
    return simple_app

def simple_app(environ, start_response):
    return handle_request(environ, start_response)

def handle_request(environ, start_response):
    method = environ['REQUEST_METHOD']
    path = environ['PATH_INFO']

    status = '200 OK'
    headers = [('Content-type','text/html')]
    encode = True

    # Sets up jinja2 to help with html templates.
    loader = jinja2.FileSystemLoader('./templates')
    jenv = jinja2.Environment(loader=loader)

    # Creates the appropriate message.
    if method == 'POST':
        if path == '/submit-post-app' or path == '/submit-post-multi':
            message = create_submit_post(environ, jenv)
        else:
            message = create_post(jenv)
    else:
        if path == '/':
            message = create_default(jenv)
        elif path == '/content':
            message = create_content(jenv)
        elif path == '/file':
            encode = False
            headers = [('Content-type', 'text/plain')]
            message = create_file()
        elif path == '/image':
            encode = False
            headers = [('Content-type', 'image/jpeg')]
            message = create_image()
        elif path == '/form-get':
            message = create_form_get(jenv)
        elif path == '/form-post-app':
            message = create_form_app(jenv)
        elif path == '/form-post-multi':
            message = create_form_multi(jenv)
        elif path == '/submit-get':
            message = create_submit(environ, jenv)
        else:
            status = '404 Not Found'
            message = create_404_error(jenv)

    start_response(status, headers) # Starts response by sending status/headers.
    # Returns rest of response.
    if(encode):
        return [message.encode('latin-1', 'replace')] # Encodes properly.
    else:
        return [message] # Don't encode for files though.

def create_default(jenv):
    return jenv.get_template('Index.html').render()

def create_content(jenv):
    return jenv.get_template('Content.html').render()

def create_file():
    return get_file('test_file.txt')

def create_image():
    return get_file('business_baby.jpg')

def create_post(jenv):
    return jenv.get_template('PostDefault.html').render()

def create_form_get(jenv):
    return jenv.get_template('FormGet.html').render()

def create_form_app(jenv):
    return jenv.get_template('FormPostApp.html').render()

def create_form_multi(jenv):
    return jenv.get_template('FormPostMulti.html').render()

def create_submit(env, jenv):
    # Parses through GET query component of URL.
    queryDict = urlparse.parse_qs(env['QUERY_STRING'])

    vars = dict(firstname=queryDict['firstname'][0],
                lastname=queryDict['lastname'][0])

    return jenv.get_template('Submit.html').render(vars)

def create_submit_post(env, jenv):
    # Holds submitted form data.
    form = cgi.FieldStorage(fp=env['wsgi.input'], environ=env)

    vars = dict(firstname=form.getvalue('firstname'),
                lastname=form.getvalue('lastname'))

    return jenv.get_template('Submit.html').render(vars)

def create_404_error(jenv):
    return jenv.get_template('404.html').render()

def get_file(filename):
    fp = open(filename, 'rb')
    filedata = fp.read()
    fp.close()
    return filedata