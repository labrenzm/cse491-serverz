# from flask_imageapp import app
from . import app
from flask import render_template, request, make_response, redirect

# from image import add_image, get_latest_image
# import image
from . import image

@app.route('/')
def show_index():
    return render_template('index.html')

@app.route('/image')
def show_image():
    return render_template('image.html')

@app.route('/all')
def show_all_images():
    num_of_imgs = image.get_num_of_images()
    return render_template('all.html', num_of_imgs=num_of_imgs)

@app.route('/upload')
def show_upload():
    return render_template('upload.html')

@app.route('/upload_receive', methods=['GET','POST'])
def upload_receive():
    if request.method == 'POST':
        the_file = request.files['file']
        data = the_file.read(int(1e9))
        image.add_image(data)

    return redirect('/')

@app.route('/image_raw')
@app.route('/image_raw/<num>')
def image_raw(num=None):
    if num:
        img = image.get_image(int(num))
    else:
        img = image.get_latest_image()
    response = make_response(img)
    response.content_type = "image/png"
    return response

