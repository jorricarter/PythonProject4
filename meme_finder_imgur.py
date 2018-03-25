# imgur api docs https://apidocs.imgur.com/
# imgur python library https://github.com/Imgur/imgurpython

from secrets import IMGUR_ID, IMGUR_SECRET
from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError
from imgurpython.imgur.models.gallery_album import GalleryAlbum
import logging


# logging setup
log = logging.getLogger(__name__)


# https://api.imgur.com/3/gallery/search?q={search term}
def get_meme(keyword, meme_only):

    logging.info("Accessing IMGUR API")

    # create api instance
    client_id = IMGUR_ID
    client_secret = IMGUR_SECRET
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
        results = client.gallery_search(
            keyword, sort=sort, window=window, page=page)
        
        memes = []
        
        for r in results:
            meme = create_meme_object(r, keyword, meme_only)
            memes.append(meme)

        logging.info("IMGUR memes: " + str(len(memes)))

        return memes

    except ImgurClientError as e:
        logging.error(e.error_message)
        logging.error(e.status_code)


def create_meme_object(meme, kw, mo):
    from classes import Meme

    title = meme.title

    # checks if meme is a GalleryAlbum object
    #   necessary because the search finds both GalleryAlbum objects and GalleryImage objects, both of which
    #   have different data structure.
    if type(meme) is GalleryAlbum:
        img_src = meme.images[0]['link']  # img source
    else:
        img_src = meme.link

    post_link = meme.link # img page

    imgur_meme = Meme(post_link, img_src, 'imgur', title, kw, mo)

    return imgur_meme


# # Enable for the command line testing
# if __name__ == "__main__":
#     keyword = input('Enter a keyword to search a meme for: ')
#     get_meme(keyword, 'on')
