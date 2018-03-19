import memeCache
from unittest import TestCase
from memeFinder import Meme, MemeCache
import os
import shutil


class TestMemeCacheModule(TestCase):

    # Tests if we can successfully pickle and unpickle data
    def test_pickle_unpickle_data(self):
        # create a test MemeCache object and create an object list for pickle/unpickle testing
        test_memecache = MemeCache('cat', True, 'source', 'memedata', 'date')
        test_memecache_2 = MemeCache('dog', True, 'source', 'memedata', 'date')
        test_memecache_list = [test_memecache, test_memecache_2]

        # pickle_data() creates directory and creates pickle file if it doesn't exist
        self.assertFalse(os.path.isdir(memeCache.cache_folder)) # verify that folder doesn't exist
        self.assertFalse(os.path.exists(memeCache.cache_file_path)) # verify that file doesn't exist

        # pickle test_memecache_list and unpickle to unpickled_cache_data
        memeCache.pickle_data(test_memecache_list)
        unpickled_cache_data = memeCache.unpickle_data()

        # It should have created folder & file
        self.assertTrue(os.path.isdir(memeCache.cache_folder))  # verify that folder has been created
        self.assertTrue(os.path.exists(memeCache.cache_file_path))  # verify that file has been created

        # test of they still have the same data after pickle/unpickling by converting
        # the MemeCache object to json/dictionary value using to_json function.
        self.assertEqual(test_memecache_list[0].to_json(), unpickled_cache_data[0].to_json())
        self.assertEqual(test_memecache_list[1].to_json(), unpickled_cache_data[1].to_json())

        # remove temp folder & file
        shutil.rmtree(memeCache.cache_folder)

    # tests if the dictionary passed from meme page will be saved and loaded properly
    def test_save_load_memebox(self):
        # Test dictionary will be changed into a Meme object and will be saved/loaded
        test_dict = {'source': 'sauce', 'title': 'champion', 'img_src': 'aaa.jpg', 'post_link': 'link'}

        # save_to_memebox() creates directory and creates pickle file if it doesn't exist
        self.assertFalse(os.path.isdir(memeCache.memebox_folder))  # verify that folder doesn't exist
        self.assertFalse(os.path.exists(memeCache.memebox_file_path))  # verify that file doesn't exist

        # save to MemeBox and load the meme data
        memeCache.save_to_memebox(test_dict)
        test_meme = memeCache.load_memebox()

        # It should have created folder & file
        self.assertTrue(os.path.isdir(memeCache.memebox_folder))  # verify that folder doesn't exist
        self.assertTrue(os.path.exists(memeCache.memebox_file_path))  # verify that file doesn't exist

        self.assertEqual(test_dict['source'], test_meme[0].source)
        self.assertTrue(test_dict['title'] == test_meme[0].title)
        self.assertEqual(test_dict['img_src'], test_meme[0].img_src)
        self.assertEqual(test_meme[0].post_link, 'link')
        self.assertIsInstance(test_meme[0], Meme)

        # remove temp folder & file
        shutil.rmtree(memeCache.memebox_folder)

    # this function removes en/decoding issues occurs during loading from/to webpage
    #   &#39;, &#34;, or \xa0 are improperly converted due to en/decoding issue
    def test_fix_annoying_amps(self):
        # create some temp Meme objects
        quote_meme = Meme('source')
        blank_meme = Meme('source')
        quote_meme.title = '&#34;Tester&#39;s agony&#34;'
        blank_meme.title = '\xa0'

        fixed_quote_meme = memeCache.fix_annoying_amps([quote_meme])
        fixed_blank_meme = memeCache.fix_annoying_amps([blank_meme])

        # fix_annoying_amps will fix the ASCII codes into proper strings " or '
        self.assertEqual(fixed_quote_meme[0].title, '"Tester\'s agony"')
        # if title was blank or \xa0, should be defaulted to 'NO TITLE'
        self.assertEqual(fixed_blank_meme[0].title, 'NO TITLE')
