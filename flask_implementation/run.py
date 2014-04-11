from flask_imageapp import app
from socket import getfqdn
from flask_imageapp import start
if __name__ == '__main__':
    start()
    host = getfqdn()
    app.run(host=host, debug=True)