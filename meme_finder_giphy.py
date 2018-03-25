# GIPHY API documents https://developers.giphy.com/docs/
# GIPHY Python client document https://github.com/Giphy/giphy-python-client !!!ditched it because it doesn't get title key

from secrets import GIPHY_KEY
import requests
import logging
import time
from urllib import parse


# logging setup
log = logging.getLogger(__name__)


# finds one downsized gif link from GIPHY using the user input as the search query
def get_meme(keyword, meme_only):

    logging.info("Accessing GIPHY API")

    try:
        base_api = "http://api.giphy.com/v1/gifs/search?"  # base api url for search
        api_key = GIPHY_KEY  # key from the secrets module
        limit = 25  # The maximum number of records to return

        # if meme only checkbox is checked, append the word 'meme'
        if meme_only == "on":
            keyword += " meme"

        # checks if keyword value is as intended.
        logging.debug("keyword: " + keyword)

        # get the json data using the api url and settings
        url = base_api + parse.urlencode({'q': keyword, 'api_key': api_key, 'limit': limit})
        logging.debug("url:" + url)  # to check for the url string
        json_data = requests.get(url).json()

        memes = []

        # create meme objects
        for entry in json_data:
            meme = create_meme_object(entry, keyword, meme_only)
            memes.append(meme)

        # Log number of memes found
        logging.info('Giphy memes: ' + str(len(json_data)))

        return memes

    except KeyError as ke:  # if there are no environment variable setup/found for GIPHY_KEY
        logging.error(ke)

    except NameError as ne:  # variable error.
        logging.error(ne)

    except TypeError as te:  # can happen with parse.urlencode if it's not set properly
        logging.error(te)

    except ValueError as ve:  # if no json data is found during requests.get
        logging.error(ve)


def create_meme_object(data, kw, mo):
    from classes import Meme
    # meme post title
    post_title = str(data['title'])

    # For <a href...> link
    post_link = data['embed_url']

    # Gets the downsized img url from the api_response
    img_src = data['images']['downsized']['url']

    giphy_meme = Meme(post_link, img_src, 'giphy', post_title, kw, mo)

    return giphy_meme



# # Used for the testing purposes
# if __name__ == "__main__":
#     keyword = input('Enter a keyword to search a meme for: ')
#     get_meme(keyword, 'on')
