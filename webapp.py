# Flask documentation http://flask.pocoo.org/docs/0.12/
# WTForms documentation https://wtforms.readthedocs.io/en/stable/

import logging
from flask import Flask, render_template, request, redirect, url_for
from wtforms import Form, StringField, validators   # Flast input validator extension module
from memeLogging import logging_setup
from memeFinder import find_meme
from memeCache import save_to_memebox, load_memebox, delete_meme


# setup logging config
logging_setup()

app = Flask(__name__)


# index page
@app.route("/")
def index():

    return render_template('index.html')


# about page
@app.route("/about")
def about():

    return render_template('about.html')


# ToDo: input validation. Possibly using WTForms
# meme page. Displays memes based on the keyword
@app.route("/meme", methods=['POST'])
def meme():

    keyword = request.form['keyword'].upper()
    meme_only = request.form.get('meme_only')

    # values debugging
    logging.debug('keyword: ' + keyword + " --search query")
    logging.debug('meme_only: ' + str(meme_only) + " --on for meme only checked/ None for unchecked")

    memes = find_meme(keyword, meme_only)

    try:
        for meme in memes:
            # logging the meme data
            logging.debug("{}: title:{} img:{} link:{}".format(meme.source.upper(), str(meme.title), meme.img_src, meme.post_link))

    except AttributeError as ae:
        logging.error(ae)
    except UnicodeEncodeError as ue:
        logging.error(ue)

    return render_template('meme.html', keyword=keyword, memes=memes)


@app.route("/memebox", methods=['POST', 'GET'])
def memebox():

    # save a meme to MemeBox if user presses the button on the meme page
    if request.method == 'POST' and list(request.form)[0] == 'source':
        meme_dict = request.form.to_dict()   # Meme object in dictionary form
        save_to_memebox(meme_dict)
        logging.info("Saved data: " + str(meme))

        # need to return something, else valueError will occur
        return "something"

    # if user presses delete button beside the meme, delete the meme
    elif request.method == 'POST' and list(request.form)[0] != 'source':

        # get the name=(MemeBox index number) of the submit button
        meme_delete = int(list(request.form)[0])

        logging.debug("index " + str(meme_delete) + " will be deleted")  # debug msg

        # delete the meme from the MemeBox using the index number
        delete_meme(meme_delete)

        # refresh MemeBox contents
        memebox_items = load_memebox()

        # And render the memebox.html using the refreshed list
        return render_template('memebox.html', memebox_items=memebox_items)

    # if user visits the MemeBox via the link at the bottom of the page
    else:
        memebox_items = load_memebox()

        return render_template('memebox.html', memebox_items=memebox_items)


if __name__ == "__main__":
    app.run()
