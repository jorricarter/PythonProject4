# imgur api docs https://apidocs.imgur.com/
# imgur python library https://github.com/Imgur/imgurpython

import random
import os
from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError
from imgurpython.imgur.models.gallery_album import GalleryAlbum
from memeFinder import Meme
import logging


# logging setup
log = logging.getLogger(__name__)


# https://api.imgur.com/3/gallery/search?q={search term}
def get_meme(keyword, meme_only):

    # create api instance
    client_id = os.environ['IMGUR_ID']
    client_secret = os.environ['IMGUR_SECRET']
    client = ImgurClient(client_id, client_secret)

    # client authorization debug
    logging.debug("imgur auth url: " + client.get_auth_url())

    # if meme only check box is selected, append meme to the keyword
    if meme_only == "on":
        keyword += " meme"

    # checks if q value is as intended. Keyword if meme only checkbox is unselected, Keyword + " meme" if selected
    logging.debug("keyword: " + keyword)

    # search parameters
    extension = 'jpg'  # jpg | png | gif | anigif (animated gif) | album Default:
    q = keyword + " ext:" + extension  # q_type extension only. Use q instead of keyword
    sort = 'viral'  # time | viral | top - defaults to time
    window = 'all'  # Change the date range of the request if the sort is 'top', day | week | month | year | all, defaults to all.
    page = 0 # integer - the data paging number

    try:
        # Search request
        memes = client.gallery_search(keyword, sort=sort, window=window, page=page)

        # gallery_search finds multiple images, so we pick one randomly from the list
        meme = random.choice(memes)

        title = meme.title

        # checks if meme is a GalleryAlbum object
        #   necessary because the search finds both GalleryAlbum objects and GalleryImage objects, both of which
        #   has different data structure.
        if type(meme) is GalleryAlbum:
            img_src = meme.images[0]['link']  # img source
        else:
            img_src = meme.link

        post_link = meme.link # img page

        imgur_meme = Meme('imgur', title, img_src, post_link)

        return imgur_meme

    except ImgurClientError as e:
        logging.error(e.error_message)
        logging.error(e.status_code)

    except IndexError as ie:
        logging.error(ie)
        return Meme('imgur')



# Enable for the command line testing
if __name__ == "__main__":
    keyword = input('Enter a keyword to search a meme for: ')
    get_meme(keyword, 'on')
