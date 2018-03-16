# Flask documentation http://flask.pocoo.org/docs/0.12/
# WTForms documentation https://wtforms.readthedocs.io/en/stable/

import memeFinderGiphy
import memeFinderImgur
import memeFinderReddit
import logging
from flask import Flask, render_template, request, redirect, url_for
from wtforms import Form, StringField, validators   # Flast input validator extension module
from memeLogging import logging_setup
from memeFinder import Meme

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

#ToDo: input validation. Possibly using WTForms
# meme page. Displays memes based on the keyword
@app.route("/meme", methods=['POST'])
def meme():

    keyword = request.form['keyword'].upper()
    meme_only = request.form.get('meme_only')

    # values debugging
    logging.debug('keyword: ' + keyword + " --search query")
    logging.debug('meme_only: ' + meme_only + " --on for meme only checked/ None for unchecked")

    # giphy/imgur/reddit meme class objects
    giphy_meme = memeFinderGiphy.get_meme(keyword, meme_only)
    imgur_meme = memeFinderImgur.get_meme(keyword, meme_only)
    reddit_meme = memeFinderReddit.get_meme(keyword, meme_only)

    try:
        # logging the meme data
        logging.debug("{}: title:{} img:{} link:{}".format(giphy_meme.source.upper(), giphy_meme.title,
                                                           giphy_meme.img_src, giphy_meme.post_link))
        logging.debug("{}: title:{} img:{} link:{}".format(imgur_meme.source.upper(), imgur_meme.title,
                                                           imgur_meme.img_src, imgur_meme.post_link))
        logging.debug("{}: title:{} img:{} link:{}".format(reddit_meme.source.upper(), reddit_meme.title,
                                                           reddit_meme.img_src, reddit_meme.post_link))

    except AttributeError as ae:
        logging.error(ae)

    return render_template('meme.html', keyword=keyword,
                           giphy_meme=giphy_meme, imgur_meme=imgur_meme, reddit_meme=reddit_meme)



if __name__ == "__main__":
    app.run()

