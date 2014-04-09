#!/usr/bin/ python
# image handling API

import os
import sqlite3
import cPickle


images = {}
return_images = []

db = sqlite3.connect('images.sqlite')



def add_image(data, filetype, name, description):
    if images:
        image_num = max(images.keys()) + 1
    else:
        image_num = 0
    db = sqlite3.connect('images.sqlite')

    # configure to allow binary insertions
    db.text_factory = bytes

    # insert!
    c = db.cursor()
    c.execute('INSERT INTO image_store (image) VALUES(?)', (data,))
    db.commit()
    db.close()
    images[image_num] = [data, filetype, name, description]

def get_image(num):
    db = sqlite3.connect('images.sqlite')
    db.text_factory = bytes
    c = db.cursor()
    #c.execute('SELECT image FROM image_store WHERE i=?', (num,))
    #num, image = c.fetchone()
    return images[num]
  
def get_search_image(num):
    return return_images[num]

def image_lookup(search_type, search_value):
    if search_type is 'name':
        for i in images:
            if search_value in images[i][2]:
                return_images.append(images[i])
    if search_type is 'description':
        for i in images:
            if search_value in images[i][3]:
                return_images.append(images[i])
    if search_type is 'either':
        for i in images:
            if search_value in images[i][2] or search_value in images[i][3]:
                return_images.append(images[i])
    return return_images
  
def clear_searches():
    del return_images[:]

def get_latest_image():
    image_num = max(images.keys())
    db = sqlite3.connect('images.sqlite')
    db.text_factory = bytes
    c = db.cursor()
    c.execute('SELECT i,image FROM image_store ORDER BY i DESC LIMIT 1')
    i, image = c.fetchone()
    db.close()
    return images[image_num]
