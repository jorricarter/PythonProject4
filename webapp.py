# Flask documentation http://flask.pocoo.org/docs/0.12/

import memeFinderGiphy
import memeFinderImgur
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


# index page
@app.route("/")
def index():

    return render_template('index.html')


# about page
@app.route("/about")
def about():

    return render_template('about.html')


# meme page. Displays memes based on the keyword
@app.route("/meme", methods=['POST'])
def meme():

    keyword = request.form['keyword'].upper()
    meme_only = request.form.get('meme_only')
    giphy_meme, giphy_meme_link = memeFinderGiphy.get_meme(keyword, meme_only)
    imgur_meme, imgur_meme_link = memeFinderImgur.get_meme(keyword, meme_only)

    return render_template('meme.html', keyword=keyword,
                           giphy_meme=giphy_meme, giphy_meme_link=giphy_meme_link,
                           imgur_meme=imgur_meme, imgur_meme_link=imgur_meme_link)


if __name__ == "__main__":
    app.run()

