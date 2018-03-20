import meme_finder_imgur
import meme_finder
import meme_cache
import os
import shutil
from unittest.mock import patch
from meme_finder import Meme, MemeCache
from unittest import TestCase, main
from imgurpython.imgur.models.gallery_album import GalleryAlbum


class TestMemeCacheModule(TestCase):

    def setUp(self):
        # cache path settings
        meme_cache.cache_folder = 'test_cache'  # cache folder name. Default = cache
        meme_cache.cache_file_name = 'cache.pickle'  # Default = cache.pickle
        meme_cache.cache_file_path = os.path.join(meme_cache.cache_folder, meme_cache.cache_file_name)

        # MemeBox path settings
        meme_cache.memebox_folder = 'test_memebox'
        meme_cache.memebox_file = 'memebox.pickle'
        meme_cache.memebox_file_path = os.path.join(meme_cache.memebox_folder, meme_cache.memebox_file)

    def tearDown(self):
        # remove temp folder & file
        if os.path.isdir(meme_cache.cache_folder):
            shutil.rmtree(meme_cache.cache_folder)
        if os.path.isdir(meme_cache.memebox_folder):
            shutil.rmtree(meme_cache.memebox_folder)

    # Tests if we can successfully pickle and unpickle data
    def test_pickle_unpickle_data(self):
        # create a test MemeCache object and create an object list for pickle/unpickle testing
        test_memecache = MemeCache('cat', True, 'source', 'memedata', 'date')
        test_memecache_2 = MemeCache('dog', True, 'source', 'memedata', 'date')
        test_memecache_list = [test_memecache, test_memecache_2]

        # pickle_data() creates directory and creates pickle file if it doesn't exist
        self.assertFalse(os.path.isdir(meme_cache.cache_folder)) # verify that folder doesn't exist
        self.assertFalse(os.path.exists(meme_cache.cache_file_path)) # verify that file doesn't exist

        # pickle test_memecache_list and unpickle to unpickled_cache_data
        meme_cache.pickle_data(test_memecache_list)
        unpickled_cache_data = meme_cache.unpickle_data()

        # It should have created folder & file
        self.assertTrue(os.path.isdir(meme_cache.cache_folder))  # verify that folder has been created
        self.assertTrue(os.path.exists(meme_cache.cache_file_path))  # verify that file has been created

        # test of they still have the same data after pickle/unpickling by converting
        # the MemeCache object to json/dictionary value using to_json function.
        self.assertEqual(test_memecache_list[0].to_json(), unpickled_cache_data[0].to_json())
        self.assertEqual(test_memecache_list[1].to_json(), unpickled_cache_data[1].to_json())

    # Tests if check_cache() will return fresh cache only
    def test_check_cache_fresh_period(self):

        expired = int(meme_cache.TODAY) - meme_cache.fresh_period   # today+fresh_period, which makes it expired
        still_okay = int(meme_cache.TODAY) - (meme_cache.fresh_period - 1)   # today+fresh_period-1, which makes it still fresh enough

        # create a test MemeCache object and create an object list
        test_memecache_fresh = MemeCache('cat', True, 'source', 'freshdata', meme_cache.TODAY)
        test_memecache_still_okay = MemeCache('cat', True, 'source', 'okaydata', still_okay)
        test_memecache_old = MemeCache('cat', True, 'source', 'olddata', expired)   # will be dropped
        test_memecache_list = [test_memecache_fresh, test_memecache_still_okay, test_memecache_old]

        # pickle test_memecache_list and unpickle to unpickled_cache_data
        meme_cache.pickle_data(test_memecache_list)
        meme_cache.unpickle_data()

        # searches for keyword=cat and meme_only=True within cache
        # fresh_meme_list would have the list of fresh/unexpired meme objects
        fresh_meme_list, old_source_list = meme_cache.check_cache('cat', True)

        # verify the test_memecache_list still contains 3 Meme objects
        self.assertEqual(len(test_memecache_list), 3)
        # verify that the fresh_meme_list only contains 2 Meme objects, dropping the test_memecache_old Meme object
        self.assertEqual(len(fresh_meme_list), 2)

        # verify that the objects in the fresh_meme_list contains correct objects
        self.assertEqual(fresh_meme_list[0].data, test_memecache_fresh.data)
        self.assertEqual(fresh_meme_list[1].data, test_memecache_still_okay.data)

    # Tests if check_cache will only return the memeCache object with the matching keyword and meme_only values
    def test_check_cache_keyword_and_meme_only(self):
        # create a test MemeCache object and create an object list
        test_memecache_keyword_meme_only = MemeCache('cat', True, 'source', 'cat true data', meme_cache.TODAY)   # both match. Should be in fresh_meme_list
        test_memecache_keyword = MemeCache('cat', False, 'source', 'cat false data', meme_cache.TODAY)   # keyword match only
        test_memecache_meme_only = MemeCache('dog', True, 'source', 'dog true data', meme_cache.TODAY)   # meme_only match only
        test_memecache_no_match = MemeCache('dog', False, 'source', 'dog false data', meme_cache.TODAY)  # no matches
        test_memecache_list = [test_memecache_keyword_meme_only, test_memecache_keyword, test_memecache_meme_only, test_memecache_no_match]

        # pickle test_memecache_list and unpickle to unpickled_cache_data
        meme_cache.pickle_data(test_memecache_list)
        meme_cache.unpickle_data()

        # searches for keyword=cat and meme_only=True within cache
        # fresh_meme_list would have the list of matching keyword/meme_only value Meme objects
        fresh_meme_list, old_meme_source = meme_cache.check_cache('cat', True)

        # verify the test_memecache_list still contains 4 Meme objects
        self.assertEqual(len(test_memecache_list), 4)
        # verify that the fresh_meme_list only contains 1 Meme object,
        self.assertEqual(len(fresh_meme_list), 1)

        # verify that the objects in the fresh_meme_list contains correct objects test_memecache_keyword_meme_only
        self.assertEqual(fresh_meme_list[0].keyword, test_memecache_keyword_meme_only.keyword)
        self.assertEqual(fresh_meme_list[0].meme_only, test_memecache_keyword_meme_only.meme_only)
        self.assertEqual(fresh_meme_list[0].data, test_memecache_keyword_meme_only.data)

    # check_cache will also return old_meme_source, the list of the sources that
    #   needs to make api request calls to get the new meme data from.
    # Test if it returns the correct list
    def test_check_cache_old_meme_source(self):

        default_sources = ['giphy', 'imgur', 'reddit']
        # try to check an empty cache and verify that old_meme_source has all 3 sources in the list
        fresh_meme_list, old_meme_source = meme_cache.check_cache('cat', True)

        # verify that old_meme_source will have 3 objects that matches default
        self.assertEqual(len(old_meme_source), 3)
        self.assertCountEqual(old_meme_source, default_sources)

        # create a test MemeCache object and create an object list
        test_memecache_giphy = MemeCache('cat', True, 'giphy', 'giphy data', meme_cache.TODAY)  # both match. Should be in fresh_meme_list
        test_memecache_imgur = MemeCache('cat', True, 'imgur', 'imgur data', meme_cache.TODAY)  # keyword match only
        test_memecache_list = [test_memecache_giphy,test_memecache_imgur]

        # pickle test_memecache_list and unpickle to unpickled_cache_data
        meme_cache.pickle_data(test_memecache_list)
        meme_cache.unpickle_data()

        # searches for keyword=cat and meme_only=True within cache
        # fresh_meme_list would have the list of    matching keyword/meme_only value Meme objects
        fresh_meme_list, old_meme_source = meme_cache.check_cache('cat', True)

        # verify that old_meme_source will have 1 object
        default_sources.remove('giphy')
        default_sources.remove('imgur')
        self.assertEqual(len(old_meme_source), 1)
        self.assertCountEqual(old_meme_source, default_sources)

    # tests if the dictionary passed from meme page will be saved and loaded properly
    def test_save_load_memebox(self):
        # Test dictionary will be changed into a Meme object and will be saved/loaded
        test_dict = {'source': 'sauce', 'title': 'champion', 'img_src': 'aaa.jpg', 'post_link': 'link'}

        # save_to_memebox() creates directory and creates pickle file if it doesn't exist
        self.assertFalse(os.path.isdir(meme_cache.memebox_folder))  # verify that folder doesn't exist
        self.assertFalse(os.path.exists(meme_cache.memebox_file_path))  # verify that file doesn't exist

        # save to MemeBox and load the meme data into test_meme
        meme_cache.save_to_memebox(test_dict)
        test_meme = meme_cache.load_memebox()

        # It should have created folder & file
        self.assertTrue(os.path.isdir(meme_cache.memebox_folder))  # verify that folder exists
        self.assertTrue(os.path.exists(meme_cache.memebox_file_path))  # verify that file exists

        # verify that test_meme list would contain Meme object created from test_dict
        self.assertIsInstance(test_meme[0], Meme)
        self.assertEqual(test_dict['source'], test_meme[0].source)
        self.assertTrue(test_dict['title'] == test_meme[0].title)
        self.assertEqual(test_dict['img_src'], test_meme[0].img_src)
        self.assertEqual(test_meme[0].post_link, 'link')
        self.assertIsInstance(test_meme[0], Meme)

    def test_load_memebox_fixes_amp_issues(self):
        #
        quotes_dict = {'source': 'sauce', 'title': '&#34;Tester&#39;s agony&#34;', 'img_src': 'aaa.jpg', 'post_link': 'link'}
        blank_dict = {'source': 'sauce', 'title': '\xa0', 'img_src': 'aaa.jpg', 'post_link': 'link'}

        # save to MemeBox and load the meme data
        meme_cache.save_to_memebox(quotes_dict)
        meme_cache.save_to_memebox(blank_dict)
        fixed_memes = meme_cache.load_memebox()

        # pickle loads data in descending order--latest saved data loads first--so, blank title object will come first
        #   followed by the quotes object. Check to see if they loads with fixed title.

        # if title was blank or \xa0, should be defaulted to 'NO TITLE'
        self.assertEqual(fixed_memes[0].title, 'NO TITLE')
        # fix_annoying_amps will fix the ASCII codes into proper strings " or '
        self.assertEqual(fixed_memes[1].title, '"Tester\'s agony"')


class TestMemeFinderModule(TestCase):

    def setUp(self):
        # cache path settings
        meme_cache.cache_folder = 'test_cache'  # cache folder name. Default = cache
        meme_cache.cache_file_name = 'cache.pickle'  # Default = cache.pickle
        meme_cache.cache_file_path = os.path.join(meme_cache.cache_folder, meme_cache.cache_file_name)

        # MemeBox path settings
        meme_cache.memebox_folder = 'test_memebox'
        meme_cache.memebox_file = 'memebox.pickle'
        meme_cache.memebox_file_path = os.path.join(meme_cache.memebox_folder, meme_cache.memebox_file)

    def tearDown(self):
        # remove temp folder & file
        if os.path.isdir(meme_cache.cache_folder):
            shutil.rmtree(meme_cache.cache_folder)
        if os.path.isdir(meme_cache.memebox_folder):
            shutil.rmtree(meme_cache.memebox_folder)

    # test if the program will find meme from api and return 3 Meme objects from each source
    def test_find_meme_api_call(self):

        # verify that there are no data in cache
        self.assertFalse(os.path.isdir(meme_cache.cache_folder))  # verify that folder doesn't exist
        self.assertFalse(os.path.exists(meme_cache.cache_file_path))  # verify that file doesn't exist

        memes = meme_finder.find_meme('cat', True)

        # verify that there are 3 Meme objects from each api sources in memes list
        self.assertEqual(len(memes), 3)

        source_list = ['giphy', 'imgur', 'reddit']
        # verify that source_list has 3 objects
        self.assertTrue(len(source_list) == 3)

        for meme in memes:
            self.assertIsInstance(meme, Meme)   # verify that all 3 objects in the list are Meme objects
            # if meme.source matches the source in source_list, remove it,
            if meme.source in source_list:
                source_list.remove(meme.source)

        # after for loop iteration, source_list should be empty
        self.assertTrue(len(source_list) == 0)

        # remove temp folder & file
        shutil.rmtree(meme_cache.cache_folder)

    # Test if find_meme will find memes from cache
    @patch('meme_finder_reddit.create_meme_object')
    @patch('meme_finder_imgur.create_meme_object')
    @patch('meme_finder_giphy.create_meme_object')
    @patch('meme_finder.get_fresh_memes')
    def test_find_meme_cache(self, mock_get_fresh_memes, mock_giphy_create_object, mock_imgur_create_object, mock_reddit_create_object) :
        # verify that there are no data in cache
        self.assertFalse(os.path.isdir(meme_cache.cache_folder))  # verify that folder doesn't exist
        self.assertFalse(os.path.exists(meme_cache.cache_file_path))  # verify that file doesn't exist

        mock_get_fresh_memes.return_value = None    # api calls won't return any new memes

        # execute find_meme function
        memes = meme_finder.find_meme('cat', True)

        # memes value should be none because it didn't get anything from the cache nor api.
        self.assertIsNone(memes)

        # create a temporary meme cache
        temp_cache = [MemeCache('cat', True, 'giphy', 'data'),
                      MemeCache('cat', True, 'imgur', 'data'),
                      MemeCache('cat', True, 'reddit', 'data')]

        # pickle the cache data and load data
        meme_cache.pickle_data(temp_cache)
        meme_cache.unpickle_data()

        # mock create_object return value because we don't have proper data in our test MemeCache objects
        # However, each function only will be evoked when there are cache data with the matching source value
        mock_giphy_create_object.return_value = Meme('giphy', 'giphy title', 'giphy img_src', 'giphy link')
        mock_imgur_create_object.return_value = Meme('imgur', 'imgur title', 'imgur img_src', 'imgur link')
        mock_reddit_create_object.return_value = Meme('reddit', 'reddit title', 'reddit img_src', 'reddit link')

        # execute find_meme function
        memes = meme_finder.find_meme('cat', True)

        # verify that there are 3 Meme objects from each api sources in memes list
        self.assertEqual(len(memes), 3)

        source_list = ['giphy', 'imgur', 'reddit']
        # verify that source_list has 3 objects
        self.assertTrue(len(source_list) == 3)

        for meme in memes:
            self.assertIsInstance(meme, Meme)  # verify that all 3 objects in the list are Meme objects
            # if meme.source matches the source in source_list, remove it,
            if meme.source in source_list:
                source_list.remove(meme.source)

        # after for loop iteration, source_list should be empty
        self.assertTrue(len(source_list) == 0)

    # tests if it will create appropriate Meme object based on it's source value
    def test_pick_meme_create_object(self):

        # create appropriate mock data value for each data.
        #   Notice that imgur data is a GalleryAlbum object instead of a dictionary
        test_giphy_data = [{'title': 'giphy title', 'images': {'downsized': {'url': 'url'}},
                            'embed_url': 'embed_url'}]
        test_imgur_data = [GalleryAlbum(title= 'imgur title', link='link', images=[{'link': 'link'}])]
        test_reddit_data = [{'title': 'reddit title', 'url':'urk', 'shortlink': 'shortlink'}]

        # create MemeCache object using the test data variables
        giphy_memecache = MemeCache('cat', True, 'giphy', test_giphy_data)
        imgur_memecache = MemeCache('cat', True, 'imgur', test_imgur_data)
        reddit_memecache = MemeCache('cat', True, 'reddit', test_reddit_data)

        # execute pick_meme
        giphy_meme = meme_finder.pick_meme(giphy_memecache)
        imgur_meme = meme_finder.pick_meme(imgur_memecache)
        reddit_meme = meme_finder.pick_meme(reddit_memecache)

        # verify that each meme are Meme objects
        self.assertIsInstance(giphy_meme, Meme)
        self.assertIsInstance(imgur_meme, Meme)
        self.assertIsInstance(reddit_meme, Meme)

        # verify that each Meme object has proper title
        self.assertEqual(giphy_meme.title, test_giphy_data[0]['title'])
        self.assertEqual(imgur_meme.title, test_imgur_data[0].title)
        self.assertEqual(reddit_meme.title, test_reddit_data[0]['title'])

    # this function removes en/decoding issues occurs during loading from/to webpage
    #   &#39;, &#34;, or \xa0 are improperly converted due to en/decoding issue
    def test_fix_annoying_amps(self):
        # create some temp Meme objects
        quote_meme = Meme('source')
        blank_meme = Meme('source')
        quote_meme.title = '&#34;Tester&#39;s agony&#34;'
        blank_meme.title = '\xa0'

        fixed_quote_meme = meme_finder.fix_annoying_amps([quote_meme])
        fixed_blank_meme = meme_finder.fix_annoying_amps([blank_meme])

        # fix_annoying_amps will fix the ASCII codes into proper strings " or '
        self.assertEqual(fixed_quote_meme[0].title, '"Tester\'s agony"')
        # if title was blank or \xa0, should be defaulted to 'NO TITLE'
        self.assertEqual(fixed_blank_meme[0].title, 'NO TITLE')


class TestMemeFinderImgur(TestCase):

    # get_meme should return the list of GalleryAlbum objects
    def test_get_meme(self):
        keyword = 'cat'
        meme_only = True

        # API call to get the meme list
        response = meme_finder_imgur.get_meme(keyword, meme_only)

        self.assertIsInstance(response, list)  # check if it's a list
        self.assertIsInstance(response[0], GalleryAlbum)   # check if the content of the list is a imgur GalleryAlbum object

    # check if create_meme_object creates Meme object
    def test_create_meme_object(self):

        meme = GalleryAlbum
        meme.title = 'title'
        meme.link = 'link'

        meme_object = meme_finder_imgur.create_meme_object(meme)

        self.assertIsInstance(meme_object, Meme)    # check if the meme_object is an actual Meme class object
        self.assertEqual(meme_object.source, 'imgur')   # check if the source is imgur
        self.assertEqual(meme_object.title, 'title')
        self.assertEqual(meme_object.img_src, 'link')
        self.assertEqual(meme_object.post_link, 'link')


if __name__ == '__main__':
    main()