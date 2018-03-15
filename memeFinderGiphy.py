# GIPHY API documents https://developers.giphy.com/docs/
# GIPHY Python client document https://github.com/Giphy/giphy-python-client



import random
import os
import re
import giphy_client
import logging
from giphy_client.rest import ApiException
from pprint import pprint


# logging setup
log = logging.getLogger(__name__)


# finds one downsized gif link from GIPHY using the user input as the search query
def get_meme(keyword, meme_only):
    # create an instance of the API class
    api_instance = giphy_client.DefaultApi()
    api_key = os.environ['GIPHY_KEY']  # str | "OUR" Giphy API Key. Need to port it to environment variable later on.
    q = keyword + " meme"  # str | Search query term or prhase.
    limit = 25  # int | The maximum number of records to return. (optional) (default to 25)
    offset = 0  # int | An optional results offset. Defaults to 0. (optional) (default to 0)
    rating = 'g'  # str | Filters results by specified rating. (optional)
    lang = 'en'  # str | Specify default country for regional content; use a 2-letter ISO 639-1 country code. See list of supported languages <a href = \"../language-support\">here</a>. (optional)
    fmt = 'json'  # str | Used to indicate the expected response format. Default is Json. (optional) (default to json)

    # if meme only checkbox is unchecked, just use the keyword without "meme" appended
    if meme_only is None:
        q = keyword

    # checks if q value is as intended. Keyword if meme only checkbox is unselected, Keyword + " meme" if selected
    logging.debug("keyword: " + q)

    try:
        # Search Endpoint
        api_response = api_instance.gifs_search_get(api_key, q, limit=limit, offset=offset, rating=rating, lang=lang,
                                                    fmt=fmt)

        # # Use it if you want a json data
        # response_json = pprint(api_response.data)
        # print(response_json)

        # randomly picks one meme
        meme = random.choice(api_response.data)

        # Gets the url from the api_response
        giphy_meme = meme.images.downsized.url
        # For some reason, <img src...> doesn't work with the trailing number after media,
        #   for instance, "https://media2.giphy.com/media/JIX9t2j0ZTN9S/giphy-downsized.gif"
        #   which is from json data, does not show picture properly.
        #   So I had to get rid of trailing number(which is random-ish; usually 1, 2, or 3) to work properly for img src
        giphy_meme = re.sub(r'media\w+', 'media', giphy_meme)

        # For <a href...> link
        giphy_meme_link = meme.embed_url

        # For reference/test for now
        # print(giphy_meme, giphy_meme_link)

        return giphy_meme, giphy_meme_link

    except ApiException as e:
        logging.error("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)
        return 'error'


# # Used for the testing purposes
# if __name__ == "__main__":
#     keyword = input('Enter a keyword to search a meme for: ')
#     get_meme(keyword, 'on')
