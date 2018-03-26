# Flask documentation http://flask.pocoo.org/docs/0.12/
# WTForms documentation https://wtforms.readthedocs.io/en/stable/

import logging
from flask import Flask, render_template, request
from wtforms import Form, StringField, BooleanField, validators   # Flask input validator extension module
from meme_logging import logging_setup
from meme_finder import find_meme
from db_sqlite import *
#from meme_cache import save_to_memebox, load_memebox, delete_meme


# setup logging config
logging_setup()

app = Flask(__name__)

user = ''

class MemeSearchForm(Form):
    keyword = StringField('keyword', [validators.Length(min=1, max=30)])    # validate input to be 1-30 characters long
    meme_only = BooleanField('meme_only')

class LoginForm(Form):
    username = StringField('username', [validators.Length(min=1, max=30)])
    password = StringField('password', [validators.Length(min=1, max=30)])


@app.route("/login", methods=['POST', 'GET'])
def login():

    login_form = LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        uname = login_form.username
        pword = login_form.password
        
        # attempt login
        try:
            # login method gets user ID
            user = login_user(uname, pword)
        
        except Exception as e:
            logging.info('Failed to log in: ' + e)

        return render_template('index.html')

    # if user visits Change User via the link at the bottom of the page
    else:
        return render_template('login.html')


# index page
@app.route("/", methods=['POST', 'GET'])
def index():

    # validate that there is no blank input
    search_form = MemeSearchForm(request.form)
    if request.method == 'POST' and search_form.validate():

        keyword = search_form.keyword.data
        meme_only = search_form.meme_only.data

        # values debugging
        logging.debug('keyword: ' + keyword + " --search query")
        logging.debug('meme_only: ' + str(meme_only) + " --on for meme only checked/ None for unchecked")

        memes = find_meme(keyword, meme_only)

        try:
            logging.debug('Memes displayed')
            for meme in memes:
                # logging the meme data
                logging.debug("id:{} source::{}: title:{} img:{} link:{}".
                             format(meme['rowid'], meme['source'].upper(), meme['post_title'], meme['img_src'],
                                    meme['post_link']))

        except AttributeError as ae:
            logging.error(ae)
        except UnicodeEncodeError as ue:
            logging.error(ue)

        return render_template('meme.html', keyword=keyword, memes=memes)

    return render_template('index.html')


# about page
@app.route("/about")
def about():

    return render_template('about.html')


# meme page. Displays memes based on the keyword
@app.route("/meme", methods=['POST'])
def meme():

    # save a meme to MemeBox if user presses the button on the meme page
    if request.method == 'POST':
        # Meme object in dictionary form
        add_to_memebox(user, meme.meme_id)
        logging.info("Saved data: " + str(meme))

        # need to return something, else valueError will occur
        return "something"


@app.route("/memebox", methods=['POST', 'GET'])
def memebox():

    # if user presses delete button beside the meme, delete the meme
    if request.method == 'POST':

        memebox_items = sel_memebox(user)

        # get the name=(MemeBox index number) of the submit button
        meme_delete = int(list(request.form)[0])

        logging.debug("index " + str(meme_delete) + " will be deleted")  # debug msg

        # delete the meme from the MemeBox using the id of the meme in the index number
        del_meme(memebox_items[meme_delete].memeId)

        # refresh MemeBox contents
        memebox_items = sel_memebox(user)

        # And render the memebox.html using the refreshed list
        return render_template('memebox.html', memebox_items=memebox_items)

    # if user visits the MemeBox via the link at the bottom of the page
    else:
        memebox_items = sel_memebox(user)

        return render_template('memebox.html', memebox_items=memebox_items)


if __name__ == "__main__":
    app.run()
