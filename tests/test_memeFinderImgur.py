import memeFinderImgur
from imgurpython.imgur.models.gallery_album import GalleryAlbum
from unittest import TestCase
from memeFinder import Meme


class TestMemeFinderImgur(TestCase):

    # get_meme should return the list of GalleryAlbum objects
    def test_get_meme(self):
        keyword = 'cat'
        meme_only = True

        # API call to get the meme list
        response = memeFinderImgur.get_meme(keyword, meme_only)

        self.assertIsInstance(response, list)  # check if it's a list
        self.assertIsInstance(response[0], GalleryAlbum)   # check if the content of the list is a imgur GalleryAlbum object

    # check if create_meme_object creates Meme object
    def test_create_meme_object(self):

        meme = GalleryAlbum
        meme.title = 'title'
        meme.link = 'link'

        meme_object = memeFinderImgur.create_meme_object(meme)

        self.assertIsInstance(meme_object, Meme)    # check if the meme_object is an actual Meme class object
        self.assertEqual(meme_object.source, 'imgur')   # check if the source is imgur
        self.assertEqual(meme_object.title, 'title')
        self.assertEqual(meme_object.img_src, 'link')
        self.assertEqual(meme_object.post_link, 'link')


