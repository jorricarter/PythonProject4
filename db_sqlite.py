import sqlite3
import logging
import time
import datetime


TODAY = time.strftime("%y%m%d")  # sets today's date into yymmdd format
# Number of days that the meme data is considered "fresh". Default = 7 days
fresh_period = 7

db = sqlite3.connect('db/gif_finder_db.db')
db.row_factory = sqlite3.Row
cur = db.cursor()


cur.execute('CREATE TABLE IF NOT EXISTS users (username text, password text)')
cur.execute('CREATE TABLE IF NOT EXISTS memecache (post_link text, img_src text, post_title text, source text, keyword text, meme_only boolean, date date)')
cur.execute('CREATE TABLE IF NOT EXISTS memebox (user_id integer, meme_id integer)')

def clear_old_cache():
    with db:
        try: 
            cur.execute('DELETE FROM memecache WHERE date < DATEADD(day, -7, ?)', (TODAY))  
            db.commit()

        except sqlite3.Error as e:
            logging.debug('SQL ERROR. Failed to clear cache.')
            logging.debug(e)


def get_fresh_cache_data(kwd, memeOnly):
    with db:
        try:
            return cur.execute('SELECT FROM memecache WHERE keyword=? and meme_only=?', (kwd, memeOnly))

        except sqlite3.Error as e:
            logging.debug('SQL ERROR. Failed searching cache.')
            logging.debug(e)


def login_user(userName, pword):
    with db:
        try:
            user = cur.execute('SELECT FROM users WHERE username=? AND password=?', (userName, pword))
            return user.rowid

        except sqlite3.Error as e:
            logging.debug('SQL ERROR. Failed to select user.')
            logging.debug(e)


def add_user(username, password):
    with db:
        try:
            cur.execute('INSERT INTO users VALUES (rowid, ?, ?)', (username, password))
            db.commit()

        except sqlite3.Error as e:
            logging.debug('SQL ERROR. Failed to add user.')
            logging.debug(e)


def del_user(userId):
    with db:
        try:
            cur.execute('DELETE FROM users WHERE user_id=?', (userId))
            db.commit()

        except sqlite3.Error as e:
            logging.debug('SQL ERROR. Failed to delete user.')
            logging.debug(e)



def check_meme_exists(imageLink):
    with db:
        try:
            return cur.execute('SELECT FROM memecache WHERE img_link=?', (imageLink))

        except sqlite3.Error as e:
            logging.debug('SQL ERROR. Failed while checking meme list.')
            logging.debug(e)


def select_meme(memeId):
    with db:
        try:
            return cur.execute('SELECT FROM memecache WHERE meme_id=?', (memeId))

        except sqlite3.Error as e:
            logging.debug('SQL ERROR. Failed to return meme object.')
            logging.debug(e)

def select_random_by_source(sourceId):
    with db:
        try:
            return cur.execute('SELECT * FROM memecache WHERE source=? IN(SELECT source FROM table ORDER BY RANDOM() LIMIT 1)', (sourceId))
            

        except sqlite3.Error as e:
            logging.debug('SQL ERROR. Failed to return meme object.')
            logging.debug(e)


def add_meme(meme):
    with db:
        try:
            cur.execute('INSERT INTO memecache VALUES (rowid, ?, ?, ?, ?, ?, ?, ?)', 
            (meme.post_link, meme.img_link, meme.post_title, meme.source, meme.keyword, meme.meme_only, meme.date))
            
            db.commit()

        except sqlite3.Error as e:
            logging.debug('SQL ERROR. Failed to add meme.')
            logging.debug(e)


def del_meme(memeId):
    with db:
        try:
            cur.execute('DELETE FROM memecache WHERE meme_id=?', (memeId))

            db.commit()

        except sqlite3.Error as e:
            logging.debug('SQL ERROR. Failed to delete meme.')
            logging.debug(e)



def sel_memebox(username):
    with db:
        try:
            logging.info("Loading " + username + "'s memebox...")
            userId = cur.execute('SELECT rowid FROM users WHERE username=?', (username))
            memebox = cur.execute('SELECT * FROM memecache WHERE rowid=?', (userId))
            return memebox

        except sqlite3.Error as e:
            logging.debug('SQL ERROR. Failed to load memebox list.')
            logging.debug(e)


def add_to_memebox(userId, memeId):
    with db:
        try:
            cur.execute('INSERT INTO memebox VALUES (?, ?)', (userId, memeId))
            logging.info("Inserted meme " + str(memeId) +
                         " into user " + str(userId) + "'s memebox")

            db.commit()

        except sqlite3.Error as e:
            logging.debug('SQL ERROR. Failed to add meme to memebox.')
            logging.debug(e)


def del_from_memebox(userId, memeId):
    with db:
        try:
            cur.execute('DELETE FROM memebox WHERE (?, ?)', (userId, memeId))
            logging.info("Deleted meme " + str(memeId) +
                         " from user " + str(userId) + "'s memebox")

            db.commit()

        except sqlite3.Error as e:
            logging.debug('SQL ERROR. Failed to delete meme from memebox.')
            logging.debug(e)



def close_db():
    with db:
        try:
            db.close()

        except sqlite3.Error as e:
            logging.debug('SQL ERROR. Failed to close database.')
            logging.debug(e)



# Checks if cache has the fresh meme data with the matching keyword, meme_only value
def retrieve_cache(keyword, meme_only):

    # delete expired=today-fresh_period from memecache table
    clear_old_cache()

    try:
        fresh_meme_data = get_fresh_cache_data(keyword, meme_only)
        logging.info('Fresh memes: ' + str(fresh_meme_data))

    except TypeError as e:
        logging.error(e)
        logging.error("No fresh memes")

    # add to old_meme_source_list if there are no fresh meme data from that source
    old_meme_source = ['giphy', 'imgur', 'reddit']

    # remove source from list if found in cache
    # https://stackoverflow.com/questions/9371114/check-if-list-of-objects-contain-an-object-with-a-certain-attribute-value
    if fresh_meme_data:
        for meme in fresh_meme_data:
            if meme.source == "giphy":
                old_meme_source.remove("giphy")
            elif meme.source == "imgur":
                old_meme_source.remove("imgur")
            elif meme.source == "reddit":
                old_meme_source.remove("reddit")

    # if there are no fresh meme in the cache
    if len(old_meme_source) > 0:
        logging.info("Could not find fresh cache from: " +
                     str(old_meme_source))

    return fresh_meme_data, old_meme_source
