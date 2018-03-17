import pickle
import os
import logging

# cache path settings
cache_folder = 'cache'  # cache folder name. Default = cache
cache_file_name = 'cache.pickle'    # Default = cache.pickle
cache_file_path = os.path.join(cache_folder, cache_file_name)

# MemeBox path settings
memebox_folder = 'memebox'
memebox_file = 'memebox.pickle'
memebox_file_path = os.path.join(memebox_folder, memebox_file)


# pickles MemeCache lists for caching data
def pickle_data(cache_data):

    # create cache_folder if not available
    try:
        # will try to create logs folder. Doesn't raise exception even if it exists
        os.makedirs(cache_folder, exist_ok=True)
    except OSError as e:
        print(e.errno)

    with open(cache_file_path, "ab") as f:
        pickle.dump(cache_data, f)


# unpickles cache data
def unpickle_data():

    try:
        cache_data = []
        with open(cache_file_path, "rb") as f:
            while True:
                try:
                    cache_data.extend(pickle.load(f))
                except EOFError:
                    break

        logging.info("cache size: " + str(len(cache_data)/3) + " sets") # one set=keyword is consist of 3 api sources
        return cache_data

    except FileNotFoundError as e:
        logging.error(e)


# When user clicks "I like this meme!" button, that meme will be saved onto the file
def save_to_memebox(meme):
    from memeFinder import Meme

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


# loads MemeBox data
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