# Flask documentation http://flask.pocoo.org/docs/0.12/

import memeFinderGiphy
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
    meme, meme_link = memeFinderGiphy.get_meme(keyword)

    return render_template('meme.html', keyword=keyword, meme=meme, meme_link=meme_link)


if __name__ == "__main__":
    app.run()

