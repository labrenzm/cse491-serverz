import sqlite3

db = sqlite3.connect('images.sqlite')
db.execute('CREATE TABLE image_store (i INTEGER PRIMARY KEY, image BLOB)');
db.commit()
db.close()