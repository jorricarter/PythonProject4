# GIPHY API documents https://developers.giphy.com/docs/
# GIPHY Python client document https://github.com/Giphy/giphy-python-client

import giphy_client
from giphy_client.rest import ApiException
from pprint import pprint


# finds one downsized gif link from GIPHY using the user input as the search query
def get_meme():
    # create an instance of the API class
    api_instance = giphy_client.DefaultApi()
    api_key = 'j5jfFyrNeH00309l3bVY2WpMeLJbXpB5'  # str | "OUR" Giphy API Key. Need to port it to environment variable later on.
    q = input('Enter a keyword to search a meme for: ')  # str | Search query term or prhase.
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

        # Gets the url from the api_response
        meme_link = api_response.data[0].images.downsized.url

        # For reference/test for now
        print(meme_link)
        return meme_link

    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)
        return 'error'


if __name__ == "__main__":
    get_meme()
