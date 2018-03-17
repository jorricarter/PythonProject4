# Flask documentation http://flask.pocoo.org/docs/0.12/
# WTForms documentation https://wtforms.readthedocs.io/en/stable/

import logging
from flask import Flask, render_template, request, redirect, url_for
from wtforms import Form, StringField, validators   # Flast input validator extension module
from memeLogging import logging_setup
from memeFinder import find_meme
from memeCache import save_to_memebox, load_memebox


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
            logging.debug("{}: title:{} img:{} link:{}".format(meme.source.upper(), meme.title, meme.img_src, meme.post_link))

    except AttributeError as ae:
        logging.error(ae)

    return render_template('meme.html', keyword=keyword, memes=memes)


@app.route("/memebox", methods=['POST', 'GET'])
def memebox():

    # save a meme to MemeBox if user presses the button
    if request.method == 'POST':
        meme = request.form.to_dict()   # Meme object in dictionary form
        save_to_memebox(meme)
        logging.info("Saved data: " + str(meme))
        return "something"  # No need to actually return useful as only gets the post when user clicks the save to memebox button

    else:
        memebox_items = load_memebox()

        return render_template('memebox.html', memebox_items=memebox_items)


if __name__ == "__main__":
    app.run()
