import quixote
from quixote.directory import Directory, export, subdir
import random
from . import html, image

comment_block = ''
no_result = ''
array_size = 0

#Credit to zhopping for TIFF implementation
class RootDirectory(Directory):
    _q_exports = []

    @export(name='')                    # this makes it public.
    def index(self):
        return html.render('index.html')

    @export(name='upload')
    def upload(self):
        return html.render('upload.html')
      
    @export(name='search')
    def search(self):
        return html.render('search.html')

    @export(name='upload_receive')
    def upload_receive(self):
      
        global image_name
        global image_description
        global metadata_string
        global not_supported
        
        request = quixote.get_request()
        print request
	
        the_file = request.form['file']
        filetype = the_file.orig_filename.split('.')[1]
        print 'Filetype = ' + filetype
        if filetype == 'tif' or filetype == 'tiff':
            filetype = 'tiff'
        if filetype == 'jpeg' or filetype == 'jpg':
            filetype = 'jpg'
        if the_file.orig_filename[-1:-3] == 'png':
            filetype ='png'
        if filetype not in 'tiftiffjpgjpegpng':
            not_supported = "Error! Filetype not supported! Please try again."
            return html.render("upload.html",globals())
        print 'received file of type: ' + filetype
        print 'received file with name:', the_file.base_filename
        data = the_file.read(int(1e9))

        image_name = request.form['image_name']
        image_description = request.form['description']
        image.add_image(data, filetype, image_name, image_description)
        
        metadata_string = """Name: \n
                             %s
                             \n
                             Description:\n
                             %s
                             
                          """%(image_name, image_description)
     
        return html.render("image.html", globals())

    @export(name='image')
    def image(self):
        return html.render('image.html')
      
    @export(name = 'search_image_count')
    def search_image_count(self):
        global array_size
        return array_size

    @export(name = 'list_of_images')
    def list_of_images(self):
        return html.render('list_of_images.html')
    
    @export(name='search_images')
    def search_images(self):
        global no_result
        global array_size
        image.clear_searches()
        request = quixote.get_request()
        if request.form['search_type'] is 'name':
            search_result = image.image_lookup('name',request.form['search_string'])
        if request.form['search_type'] is 'description':
            search_result = image.image_lookup('description',request.form['search_string'])
        else:
            search_result = image.image_lookup('either', request.form['search_string'])

        if not search_result:  #checking to see if any images were returned from search
            global no_result
            no_result = "Sorry, no results found!"
            return html.render("search.html", globals())
        else:
            array_size = len(search_result)
            
            return html.render("search_results.html")

    @export(name='image_raw')
    def image_raw(self):
        response = quixote.get_response()
        request = quixote.get_request()
        try:
            img = image.get_image(int(request.form['num']))
        except KeyError:
            img = image.get_latest_image()
        response.set_content_type('image/%s' % img[1])
        
        return img[0]
      
    @export(name='search_image_raw')
    def search_image_raw(self):
        
        response = quixote.get_response()
        request = quixote.get_request()

        img = image.get_search_image(int(request.form['num']))
        response.set_content_type('image/%s' % img[1])
        return img[0]
    
    @export(name = 'image_count')
    def image_count(self):
        return len(image.images)
    
    @export(name='jquery')
    def jquery(self):
        return open('jquery-1.3.2.min.js').read()
    
    @export(name = 'submit_comment')
    def submit_comment(self):
        global comment_block
        random_names = {}
        random_names[0] = 'Shaky Photographer'
        random_names[1] = 'Nervous Toupee-Maker'
        random_names[2] = 'Jazzy Hobo'
        random_names[3] = 'Pudding Psychologist'
        random_names[4] = 'Bungalow Developer'
        random_names[5] = 'Omniscient Geologist'
        random_names[6] = 'Cashew Accountant'
        
        request = quixote.get_request()
        comment = request.form['comment']
        comment = random_names[(random.randint(0,6))] + ': '+ comment+"<br>"
            
        comment_block += comment
        return html.render("image.html", globals())
