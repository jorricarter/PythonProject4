import _pickle
import os
import logging
import time


# Path setting ######################################################################################################

# cache path settings
cache_folder = 'cache'  # cache folder name. Default = cache
cache_file_name = 'cache.pickle'    # Default = cache.pickle
cache_file_path = os.path.join(cache_folder, cache_file_name)

# MemeBox path settings
memebox_folder = 'memebox'
memebox_file = 'memebox.pickle'
memebox_file_path = os.path.join(memebox_folder, memebox_file)


# Cache #############################################################################################################

TODAY = time.strftime("%y%m%d")  # sets today's date into yymmdd format
fresh_period = 7    # Number of days that the meme data is considered "fresh". Default = 7 days

# pickles MemeCache lists for caching data
def pickle_data(cache_data):
    # create cache_folder if not available
    try:
        # will try to create logs folder. Doesn't raise exception even if it exists
        os.makedirs(cache_folder, exist_ok=True)
    except OSError as e:
        logging.error(e.errno)

    if cache_data is not None:
        with open(cache_file_path, "ab") as f:
            _pickle.dump(cache_data, f)


# unpickles cache data
def unpickle_data():
    try:
        cache_data = []
        with open(cache_file_path, "rb") as f:
            while True:
                try:
                    cache_data.extend(_pickle.load(f))
                except EOFError:
                    break

        logging.info(
            "cache size: " + str(int(len(cache_data) / 3)) + " set(s)")  # one set=keyword is consist of 3 api sources
        return cache_data

    except FileNotFoundError as e:
        logging.error(e)


# Checks if cache has the fresh meme data with the matching keyword, meme_only value
def check_cache(keyword, meme_only):

    # unpickles cache file
    try:
        cache_data = unpickle_data()
    except TypeError as e:
        logging.error(e)
        logging.error("No meme cache data")
        cache_data = None

    # delete expired=today-fresh_period memeCache data
    delete_old_cache(cache_data)

    # if the MemeCache with the matching keyword, meme_only value and within the fresh period,
    #   add to fresh_meme_data list
    fresh_meme_data = []
    try:
        for cache in cache_data:
            if cache.keyword == keyword and cache.meme_only == meme_only:
                fresh_meme_data.append(cache)
    except TypeError as e:
        logging.error(e)
        logging.error("No fresh memes")

    # add to old_meme_source_list if there are no fresh meme data from that source
    old_meme_source = ['giphy', 'imgur', 'reddit']

    # https://stackoverflow.com/questions/9371114/check-if-list-of-objects-contain-an-object-with-a-certain-attribute-value
    for meme in fresh_meme_data:
        if meme.source == "giphy":
            old_meme_source.remove("giphy")
        elif meme.source == "imgur":
            old_meme_source.remove("imgur")
        elif meme.source == "reddit":
            old_meme_source.remove("reddit")

    # if there are no fresh meme in the cache
    if len(old_meme_source) > 0:
        logging.info("Could not find fresh cache from: " + str(old_meme_source))

    return fresh_meme_data, old_meme_source


# delete expired cache to reduce cache size
def delete_old_cache(cache_data):

    try:
        # remove from the cache_data if it has expired
        for cache in cache_data:
            if int(cache.date) + fresh_period <= int(TODAY):
                cache_data.remove(cache)

        # if there were cache_data originally, overwrite cache data with the new cache data without expired data
        if len(cache_data) is not None:
            with open(cache_file_path, "wb") as f:
                _pickle.dump(cache_data, f)

    except TypeError as e:
        logging.error(e)
        logging.error("No cache data")

    return cache_data


# MemeBox ###########################################################################################################


# When user clicks "I like this meme!" button, that meme will be saved onto the file
def save_to_memebox(meme_dict):
    from memeFinder import Meme

    # create Meme class object from dictionary
    meme = Meme(meme_dict['source'], meme_dict['title'], meme_dict['img_src'], meme_dict['post_link'])

    # create cache_folder if not available
    try:
        # will try to create logs folder. Doesn't raise exception even if it exists
        os.makedirs(memebox_folder, exist_ok=True)
    except OSError as e:
        logging.error(e.errno)

    with open(memebox_file_path, "ab") as f:
        _pickle.dump(meme, f)


# loads MemeBox data
def load_memebox():
    from memeFinder import fix_annoying_amps

    try:
        memes = []
        with open(memebox_file_path, "rb") as f:
            while True:
                try:
                    # load the initial load into temp_load for if statement
                    temp_load = _pickle.load(f)
                    # if temp_load is instance of list, extend the memes list
                    #   else, it's a Meme object, so we append to the memes list
                    if isinstance(temp_load, list):
                        memes.extend(temp_load)
                    else:
                        memes.append(temp_load)

                # if it's end of the file, break the loop
                except EOFError:
                    break

        logging.info("MemeBox size: " + str(len(memes)))
        memes.reverse()  # make sure the latest meme comes on top

        memes = fix_annoying_amps(memes)

        return memes

    except FileNotFoundError as e:
        logging.error(e)


# When user clicks delete button from the MemeBox, delete the meme from the list/MemeBox
def delete_meme(index):
    memes = load_memebox()

    del memes[index]
    logging.info("Meme deleted")

    memes.reverse()  # make sure memes would be saved as ascending order

    # overwrite the file with the meme-deleted list
    with open(memebox_file_path, "wb") as f:
        _pickle.dump(memes, f)
