# Flask documentation http://flask.pocoo.org/docs/0.12/
# WTForms documentation https://wtforms.readthedocs.io/en/stable/

import memeFinderGiphy
import memeFinderImgur
import memeFinderReddit
import logging
from flask import Flask, render_template, request, redirect, url_for
from wtforms import Form, StringField, validators   # Flast input validator extension module
from memeLogging import logging_setup

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

    # giphy/imgur/reddit img and the post links
    giphy_meme, giphy_meme_link = memeFinderGiphy.get_meme(keyword, meme_only)
    imgur_meme, imgur_meme_link = memeFinderImgur.get_meme(keyword, meme_only)
    reddit_meme, reddit_meme_link = memeFinderReddit.get_meme(keyword, meme_only)

    # logging the meme img and the page links
    logging.debug("GIPHY: img:{} link:{}".format(giphy_meme, giphy_meme_link))
    logging.debug("IMGUR: img:{} link:{}".format(imgur_meme, imgur_meme_link))
    logging.debug("REDDIT: img:{} link:{}".format(reddit_meme, reddit_meme_link))

    return render_template('meme.html', keyword=keyword,
                           giphy_meme=giphy_meme, giphy_meme_link=giphy_meme_link,
                           imgur_meme=imgur_meme, imgur_meme_link=imgur_meme_link,
                           reddit_meme=reddit_meme, reddit_meme_link=reddit_meme_link)


if __name__ == "__main__":
    app.run()

