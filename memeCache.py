import _pickle
import os
import logging


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


# pickles MemeCache lists for caching data
def pickle_data(cache_data):

    # create cache_folder if not available
    try:
        # will try to create logs folder. Doesn't raise exception even if it exists
        os.makedirs(cache_folder, exist_ok=True)
    except OSError as e:
        print(e.errno)

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

        logging.info("cache size: " + str(int(len(cache_data)/3)) + " set(s)") # one set=keyword is consist of 3 api sources
        return cache_data

    except FileNotFoundError as e:
        logging.error(e)


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
        print(e.errno)

    with open(memebox_file_path, "ab") as f:
        _pickle.dump(meme, f)


# loads MemeBox data
def load_memebox():

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


