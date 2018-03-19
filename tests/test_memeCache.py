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

    # Tests if check_cache() will return fresh cache only
    def test_check_cache_fresh_period(self):

        expired = int(memeCache.TODAY) - memeCache.fresh_period   # today+fresh_period, which makes it expired
        still_okay = int(memeCache.TODAY) - (memeCache.fresh_period -1)   # today+fresh_period-1, which makes it still fresh enough

        # create a test MemeCache object and create an object list
        test_memecache_fresh = MemeCache('cat', True, 'source', 'freshdata', memeCache.TODAY)
        test_memecache_still_okay = MemeCache('cat', True, 'source', 'okaydata', still_okay)
        test_memecache_old = MemeCache('cat', True, 'source', 'olddata', expired)   # will be dropped
        test_memecache_list = [test_memecache_fresh, test_memecache_still_okay, test_memecache_old]

        # pickle test_memecache_list and unpickle to unpickled_cache_data
        memeCache.pickle_data(test_memecache_list)
        memeCache.unpickle_data()

        # searches for keyword=cat and meme_only=True within cache
        # fresh_meme_list would have the list of fresh/unexpired meme objects
        fresh_meme_list, old_source_list = memeCache.check_cache('cat', True)

        # verify the test_memecache_list still contains 3 Meme objects
        self.assertEqual(len(test_memecache_list), 3)
        # verify that the fresh_meme_list only contains 2 Meme objects, dropping the test_memecache_old Meme object
        self.assertEqual(len(fresh_meme_list), 2)

        # verify that the objects in the fresh_meme_list contains correct objects
        self.assertEqual(fresh_meme_list[0].data, test_memecache_fresh.data)
        self.assertEqual(fresh_meme_list[1].data, test_memecache_still_okay.data)

        # remove temp folder & file
        shutil.rmtree(memeCache.cache_folder)

    # Tests if check_cache will only return the memeCache object with the matching keyword and meme_only values
    def test_check_cache_keyword_and_meme_only(self):
        # create a test MemeCache object and create an object list
        test_memecache_keyword_meme_only = MemeCache('cat', True, 'source', 'cat true data', memeCache.TODAY)   # both match. Should be in fresh_meme_list
        test_memecache_keyword = MemeCache('cat', False, 'source', 'cat false data', memeCache.TODAY)   # keyword match only
        test_memecache_meme_only = MemeCache('dog', True, 'source', 'dog true data', memeCache.TODAY)   # meme_only match only
        test_memecache_no_match = MemeCache('dog', False, 'source', 'dog false data', memeCache.TODAY)  # no matches
        test_memecache_list = [test_memecache_keyword_meme_only, test_memecache_keyword, test_memecache_meme_only, test_memecache_no_match]

        # pickle test_memecache_list and unpickle to unpickled_cache_data
        memeCache.pickle_data(test_memecache_list)
        memeCache.unpickle_data()

        # searches for keyword=cat and meme_only=True within cache
        # fresh_meme_list would have the list of matching keyword/meme_only value Meme objects
        fresh_meme_list, old_meme_source = memeCache.check_cache('cat', True)

        # verify the test_memecache_list still contains 4 Meme objects
        self.assertEqual(len(test_memecache_list), 4)
        # verify that the fresh_meme_list only contains 1 Meme object,
        self.assertEqual(len(fresh_meme_list), 1)

        # verify that the objects in the fresh_meme_list contains correct objects test_memecache_keyword_meme_only
        self.assertEqual(fresh_meme_list[0].keyword, test_memecache_keyword_meme_only.keyword)
        self.assertEqual(fresh_meme_list[0].meme_only, test_memecache_keyword_meme_only.meme_only)
        self.assertEqual(fresh_meme_list[0].data, test_memecache_keyword_meme_only.data)

        # remove temp folder & file
        shutil.rmtree(memeCache.cache_folder)

    # check_cache will also return old_meme_source, the list of the sources that
    #   needs to make api request calls to get the new meme data from.
    # Test if it returns the correct list
    def test_check_cache_old_meme_source(self):

        default_sources = ['giphy', 'imgur', 'reddit']
        # try to check an empty cache and verify that old_meme_source has all 3 sources in the list
        fresh_meme_list, old_meme_source = memeCache.check_cache('cat', True)

        # verify that old_meme_source will have 3 objects that matches default
        self.assertEqual(len(old_meme_source), 3)
        self.assertCountEqual(old_meme_source, default_sources)

        # create a test MemeCache object and create an object list
        test_memecache_giphy = MemeCache('cat', True, 'giphy', 'giphy data', memeCache.TODAY)  # both match. Should be in fresh_meme_list
        test_memecache_imgur = MemeCache('cat', True, 'imgur', 'imgur data', memeCache.TODAY)  # keyword match only
        test_memecache_list = [test_memecache_giphy,test_memecache_imgur]

        # pickle test_memecache_list and unpickle to unpickled_cache_data
        memeCache.pickle_data(test_memecache_list)
        memeCache.unpickle_data()

        # searches for keyword=cat and meme_only=True within cache
        # fresh_meme_list would have the list of    matching keyword/meme_only value Meme objects
        fresh_meme_list, old_meme_source = memeCache.check_cache('cat', True)

        # verify that old_meme_source will have 1 object
        default_sources.remove('giphy')
        default_sources.remove('imgur')
        self.assertEqual(len(old_meme_source), 1)
        self.assertCountEqual(old_meme_source, default_sources)

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

    def test_load_memebox_fixes_amp_issues(self):
        #
        quotes_dict = {'source': 'sauce', 'title': '&#34;Tester&#39;s agony&#34;', 'img_src': 'aaa.jpg', 'post_link': 'link'}
        blank_dict = {'source': 'sauce', 'title': '\xa0', 'img_src': 'aaa.jpg', 'post_link': 'link'}

        # save to MemeBox and load the meme data
        memeCache.save_to_memebox(quotes_dict)
        memeCache.save_to_memebox(blank_dict)
        fixed_memes = memeCache.load_memebox()

        # pickle loads data in descending order--latest saved data loads first--so, blank title object will come first
        #   followed by the quotes object. Check to see if they loads with fixed title.

        # if title was blank or \xa0, should be defaulted to 'NO TITLE'
        self.assertEqual(fixed_memes[0].title, 'NO TITLE')
        # fix_annoying_amps will fix the ASCII codes into proper strings " or '
        self.assertEqual(fixed_memes[1].title, '"Tester\'s agony"')

        # remove temp folder & file
        shutil.rmtree(memeCache.memebox_folder)
