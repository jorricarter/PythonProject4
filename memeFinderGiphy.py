# GIPHY API documents https://developers.giphy.com/docs/
# GIPHY Python client document https://github.com/Giphy/giphy-python-client

import os
import re
import giphy_client
from giphy_client.rest import ApiException
from pprint import pprint


# finds one downsized gif link from GIPHY using the user input as the search query
def get_meme(keyword):
    # create an instance of the API class
    api_instance = giphy_client.DefaultApi()
    api_key = os.environ['GIPHY_KEY']  # str | "OUR" Giphy API Key. Need to port it to environment variable later on.
    q = keyword  # str | Search query term or prhase.
    limit = 1  # int | The maximum number of records to return. (optional) (default to 25)
    offset = 0  # int | An optional results offset. Defaults to 0. (optional) (default to 0)
    rating = 'g'  # str | Filters results by specified rating. (optional)
    lang = 'en'  # str | Specify default country for regional content; use a 2-letter ISO 639-1 country code. See list of supported languages <a href = \"../language-support\">here</a>. (optional)
    fmt = 'json'  # str | Used to indicate the expected response format. Default is Json. (optional) (default to json)

    try:
        # Search Endpoint
        api_response = api_instance.gifs_search_get(api_key, q, limit=limit, offset=offset, rating=rating, lang=lang,
                                                    fmt=fmt)

        # # Use it if you want a json data
        # response_json = pprint(api_response)
        # print(response_json)

        # Gets the url from the api_response
        meme = api_response.data[0].images.downsized.url
        # For some reason, <img src...> doesn't work with the trailing number after media,
        #   for instance, "https://media2.giphy.com/media/JIX9t2j0ZTN9S/giphy-downsized.gif"
        #   which is from json data, does not show picture properly.
        #   So I had to get rid of trailing number(which is random-ish; usually 1 or 2) to work properly for img src
        meme = re.sub(r'media\w+', 'media', meme)

        # For <a href...> link
        meme_link = api_response.data[0].embed_url

        # For reference/test for now
        print(meme, meme_link)
        return meme, meme_link

    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)
        return 'error'

# Used for the testing purposes
# if __name__ == "__main__":
#     keyword = input('Enter a keyword to search a meme for: ')
#     get_meme(keyword)
