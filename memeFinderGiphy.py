# GIPHY API documents https://developers.giphy.com/docs/
# GIPHY Python client document https://github.com/Giphy/giphy-python-client !!!ditched it because it doesn't get title key

from secrets import GIPHY_KEY
import requests
import logging
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

        return json_data['data']

    except KeyError as ke:  # if there are no environment variable setup/found for GIPHY_KEY
        logging.error(ke)

    except NameError as ne:  # variable error.
        logging.error(ne)

    except TypeError as te:  # can happen with parse.urlencode if it's not set properly
        logging.error(te)

    except ValueError as ve:  # if no json data is found during requests.get
        logging.error(ve)


def create_meme_object(meme):
    from memeFinder import Meme
    # meme post title
    title = str(meme['title'])

    # Gets the downsized img url from the api_response
    img_src = meme['images']['downsized']['url']

    # For <a href...> link
    post_link = meme['embed_url']

    giphy_meme = Meme('giphy', title, img_src, post_link)

    return giphy_meme


# # Used for the testing purposes
# if __name__ == "__main__":
#     keyword = input('Enter a keyword to search a meme for: ')
#     get_meme(keyword, 'on')
