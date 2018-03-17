import time
import pickle
import os
import memeFinderGiphy
import memeFinderImgur
import memeFinderReddit
import random
import logging
import json


log = logging.getLogger(__name__)

TODAY = time.strftime("%y%m%d")  # sets today's date into yymmdd format
fresh_period = 7    # Number of days that the meme data is considered "fresh". Default = 7 days

cache_folder = 'cache'  # cache folder name. Default = cache
cache_file_name = 'cache.pickle'    # Default = cache.pickle
cache_file_path = os.path.join(cache_folder, cache_file_name)

memebox_folder = 'memebox'
memebox_file = 'memebox.pickle'
memebox_file_path = os.path.join(memebox_folder, memebox_file)


# Meme class object
class Meme:
    def __init__(self, source, title="No results", img_src="", post_link="/"):
        self.source = source    # where it originated from (giphy/imgur/reddit)
        self.title = title      # post title
        self.img_src = img_src    # direct image link
        self.post_link = post_link  # post link

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)


# Holds the JSON data and other info to save within the cache
class MemeCache:
    def __init__(self, keyword, meme_only, source, data, date=TODAY):
        self.keyword = keyword
        self.meme_only = meme_only
        self.source = source
        self.data = data    # from API requeest
        self.date = date    # date that's created

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)


# main function to find meme with the keyword and meme_only value option
def find_meme(keyword, meme_only):

    # checks for the cache with the keyword and meme_only value
    fresh_meme_data, old_meme_source_list = check_cache(keyword, meme_only)

    # if sources are found in old_meme_source_list, refresh cache for that source
    for source in old_meme_source_list:
        fresh_meme_data.append(refresh_cache(keyword, meme_only, source))

    # picks one meme from each source
    memes = []
    for meme_data in fresh_meme_data:
        memes.append(pick_meme(meme_data))

    # if cache has been refreshed, update cache
    if len(old_meme_source_list) > 0:
        pickle_data(fresh_meme_data)

    for meme in memes:
        print(meme.to_json())

    return memes


# Checks if cache has the fresh meme data with the matching keyword, meme_only value
def check_cache(keyword, meme_only):

    # unpickles cache file
    try:
        cache_data = unpickle_data()
    except TypeError as e:
        logging.error(e)
        cache_data = None

    # if the MemeCache with the matching keyword, meme_only value and within the fresh period,
    #   add to fresh_meme_data list
    fresh_meme_data = []
    try:
        for cache in cache_data:
            if cache.keyword == keyword and cache.meme_only == meme_only and int(cache.date) + fresh_period >= int(TODAY):
                fresh_meme_data.append(cache)
    except TypeError as e:
        logging.error(e)
        logging.error("No fresh memes")

    # add to old_meme_source_list if there are no fresh meme data from that source
    old_meme_source = ['giphy', 'imgur', 'reddit']

    # https://stackoverflow.com/questions/9371114/check-if-list-of-objects-contain-an-object-with-a-certain-attribute-value
    if any(x.source == "giphy" for x in fresh_meme_data):
        old_meme_source.remove('giphy')
    if any(x.source == "imgur" for x in fresh_meme_data):
        old_meme_source.remove('imgur')
    if any(x.source == "reddit" for x in fresh_meme_data):
        old_meme_source.remove('reddit')

    # if there are no fresh meme in the cache
    if len(old_meme_source) > 0:
        logging.info("Could not find fresh cache from: " + str(old_meme_source))

    return fresh_meme_data, old_meme_source


# If there are no fresh meme found on cache, get a new meme data from the appropriate source
def refresh_cache(keyword, meme_only, source):

    if source == 'giphy':
        meme_data = memeFinderGiphy.get_meme(keyword, meme_only)
    elif source == 'imgur':
        meme_data = memeFinderImgur.get_meme(keyword, meme_only)
    else:
        meme_data = memeFinderReddit.get_meme(keyword, meme_only)

    # create a MemeCache object with the new meme_data
    fresh_meme_cache = MemeCache(keyword, meme_only, source, meme_data)

    return fresh_meme_cache


# picks one meme randomly from the meme_data
def pick_meme(meme_data):

    try:
        meme = random.choice(meme_data.data)

        if meme_data.source == 'giphy':
            return memeFinderGiphy.create_meme_object(meme)

        elif meme_data.source == 'imgur':
            return memeFinderImgur.create_meme_object(meme)

        else:
            return memeFinderReddit.create_meme_object(meme)

    except IndexError as ie:  # if search didn't find any result with tht keyword
        logging.error(ie)
        logging.info("No meme data found. Creating a default Meme object")
        return Meme(meme_data.source)


def pickle_data(cache_data):

    # create cache_folder if not available
    try:
        # will try to create logs folder. Doesn't raise exception even if it exists
        os.makedirs(cache_folder, exist_ok=True)
    except OSError as e:
        print(e.errno)

    with open(cache_file_path, "ab") as f:
        pickle.dump(cache_data, f)


def unpickle_data():

    try:
        cache_data = []
        with open(cache_file_path, "rb") as f:
            while True:
                try:
                    cache_data.extend(pickle.load(f))
                except EOFError:
                    break

        logging.info("cache size: " + str(len(cache_data)))
        logging.info(cache_data)
        return cache_data

    except FileNotFoundError as e:
        logging.error(e)


# When user clicks "I like this meme!" button, that meme will be saved onto the file
def save_to_memebox(meme):

    # create Meme class object from dictionary
    meme = Meme(meme['source'], meme['title'], meme['img_src'], meme['post_link'])

    # create cache_folder if not available
    try:
        # will try to create logs folder. Doesn't raise exception even if it exists
        os.makedirs(memebox_folder, exist_ok=True)
    except OSError as e:
        print(e.errno)

    with open(memebox_file_path, "ab") as f:
        pickle.dump(meme, f)


def load_memebox():

    try:
        memes = []
        with open(memebox_file_path, "rb") as f:
            while True:
                try:
                    memes.append(pickle.load(f))
                except EOFError:
                    break

        logging.info("MemeBox size: " + str(len(memes)))
        return memes

    except FileNotFoundError as e:
        logging.error(e)