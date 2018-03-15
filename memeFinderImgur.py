# imgur api docs https://apidocs.imgur.com/
# imgur python library https://github.com/Imgur/imgurpython

import random
import os
from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError
from pprint import pprint


# https://api.imgur.com/3/gallery/search?q={search term}
def get_meme(keyword, meme_only):

    # create api instance
    client_id = os.environ['IMGUR_ID']
    client_secret = os.environ['IMGUR_SECRET']
    client = ImgurClient(client_id, client_secret)

    # if meme only check box is selected, append meme to the keyword
    if meme_only is "on":
        keyword += " meme"

    # search parameters
    extension = 'jpg'  # jpg | png | gif | anigif (animated gif) | album Default:
    q = keyword + " ext:" + extension  # q_type extension only
    sort = 'viral' # time | viral | top - defaults to time
    window = 'all' # Change the date range of the request if the sort is 'top', day | week | month | year | all, defaults to all.
    page = 0 # integer - the data paging number

    try:
        # Search request
        items = client.gallery_search(q, sort=sort, window=window, page=page)

        # gallery_search finds multiple images, so we pick one randomly from the list
        item = random.choice(items)

        imgur_meme = item.images[0]['link'] # img source
        imgur_meme_link = item.link # img page

        return imgur_meme, imgur_meme_link

    except ImgurClientError as e:
        print(e.error_message)
        print(e.status_code)


# # Enable for the command line testing
# if __name__ == "__main__":
#     keyword = input('Enter a keyword to search a meme for: ')
#     get_meme(keyword, 'on')
