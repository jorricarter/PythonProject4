import time
import random
import logging
import json
import memeFinderGiphy
import memeFinderImgur
import memeFinderReddit
import concurrent.futures
from memeCache import pickle_data, check_cache, TODAY


# turn on logging
log = logging.getLogger(__name__)


# Objects ##########################################################################################################

# Meme class object:
class Meme:
    def __init__(self, source="No source", title="No results", img_src="", post_link="/"):
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


# Functions #######################################################################################################

# main function to find meme with the keyword and meme_only value option
def find_meme(keyword, meme_only):

    logging.info("Looking for dank memes for keyword:{} meme_only:{}".format(keyword, str(meme_only)))

    # Speed comparison test.
    threading_speed_test_on = False  # switch to True is you want to test. WARNING: switch back to False after testing.
    if threading_speed_test_on:
        test_api_call_speed_with_threading_and_without_threading()

    # checks for the cache with the keyword and meme_only value
    fresh_meme_data, old_meme_source_list = check_cache(keyword, meme_only)

    # if sources are found in old_meme_source_list, get fresh memes from each API and refresh cache
    if len(old_meme_source_list) > 0:
        fresh_meme_data = get_fresh_memes(fresh_meme_data, old_meme_source_list, keyword, meme_only)
        pickle_data(fresh_meme_data)
    else:
        logging.info("Pulling (keyword:{} meme_only:{}) search results from cache".format(keyword, str(meme_only)))

    # picks one meme from each source
    memes = [pick_meme(next(meme_data for meme_data in fresh_meme_data if meme_data.source == 'giphy')),
             pick_meme(next(meme_data for meme_data in fresh_meme_data if meme_data.source == 'imgur')),
             pick_meme(next(meme_data for meme_data in fresh_meme_data if meme_data.source == 'reddit'))]

    # debug purposes to see the memes
    for meme in memes:
        logging.debug("find_meme(): " + meme.to_json())

    return memes


# Make API request calls to get new meme data if there are no fresh memes from the list
def get_fresh_memes(fresh_meme_data, old_meme_source_list, keyword, meme_only):
    num_threads = 3  # Number of threads to run in parallel

    start_time = time.time()    # start timer

    # Concurrent execution
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = {executor.submit(
            fresh_meme_data.append(api_call(keyword, meme_only, source))
        ) for source in old_meme_source_list}
        concurrent.futures.wait(futures)

    end_time = time.time()  # end timer

    logging.info("Execution time: %s" % (end_time - start_time))

    return fresh_meme_data


# If there are no fresh meme found on cache, get a new meme data from the appropriate source
def api_call(keyword, meme_only, source):

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


# fix the annoying en/decoding issue with amps/ASCII
def fix_annoying_amps(memes):

    # extracts the titles from the memes list to work with
    title_list = list(map(lambda meme: meme.title, memes))

    # replaces annoying &#34; and &#39; from the title list
    replace_single_quote = list(map(lambda title: title.replace("&#39;", "'"), title_list))
    replace_double_quote = list(map(lambda title: title.replace("&#34;", "\""), replace_single_quote))
    replace_blank = list(map(lambda title: title.replace("\xa0", "NO TITLE"), replace_double_quote))

    title_list = replace_blank

    # update the title with the fixed title
    for x in range(len(memes)):
        memes[x].title = title_list[x]

    # returns fixed memes list
    return memes


# Testing Functions ################################################################################################

# for testing purposes. No need for the actual production
def test_api_call_speed_with_threading_and_without_threading():
    logging.info("######Threading speed test starts here######")

    no_thread_duration = []
    with_thread_duration = []

    for x in range(10):
        no_thread_duration.append(test_no_threading())
        with_thread_duration.append(test_with_threading())

    avg_no_thread_duration = sum(no_thread_duration)/len(no_thread_duration)
    avg_with_thread_duration = sum(with_thread_duration)/len(with_thread_duration)
    performance = (((avg_no_thread_duration/avg_with_thread_duration) - 1) * 100)

    logging.info("times without threading:")
    for test in no_thread_duration:
        logging.info(test)

    logging.info("times with threading:")
    for test in with_thread_duration:
        logging.info(test)

    logging.info("Average duration:")
    logging.info("Without threading: " + str(avg_no_thread_duration))
    logging.info("With threading: " + str(avg_with_thread_duration))

    logging.info("Threading is faster than no threading by {}%!".format(performance, '.2f'))

    logging.info("######Threading speed test ends here######")


def test_no_threading():
    fresh_meme_data = []
    old_meme_source_list = ['giphy', 'imgur', 'reddit']
    keyword = 'cat'
    meme_only = 'on'

    start_time = time.time()

    for source in old_meme_source_list:
        fresh_meme_data.append(api_call(keyword, meme_only, source))

    end_time = time.time()

    no_threading_duration = end_time - start_time

    return no_threading_duration


def test_with_threading():
    fresh_meme_data = []
    old_meme_source_list = ['giphy', 'imgur', 'reddit']
    keyword = 'cat'
    meme_only = 'on'

    num_threads = 3
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = {executor.submit(
            fresh_meme_data.append(api_call(keyword, meme_only, source))
        ) for source in old_meme_source_list}
        concurrent.futures.wait(futures)

    end_time = time.time()

    with_threading_duration = end_time - start_time

    return with_threading_duration


# unused for now, but may modify/use to test if we can shrink cache size
def convert_meme_object_to_dict(memes):
    meme_dict = []
    for meme in memes:
        meme_dict.append({'source': meme.source, 'title': meme.title, 'img_src': meme.img_src, 'post_link': meme.post_link})

    return meme_dict
