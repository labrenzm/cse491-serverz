from flask import  Flask
app = Flask(__name__)

from . import image

def start():
    try:
        some_data = open('flask_imageapp/tux.png', 'rb').read()
    except IOError:
        some_data = open('kerm.jpg', 'rb').read()
    image.add_image(some_data)

# import flask_imageapp.views
import views