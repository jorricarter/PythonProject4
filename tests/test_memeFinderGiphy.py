import memeFinderGiphy
import unittest
import os
import requests
from unittest import TestCase
from unittest import mock
from unittest.mock import Mock
from unittest.mock import patch


class TestGetMeme(unittest.TestCase):

    # def setUp(self):
    #    # FILLER TO SHUT PYCHARM UP UNTIL I FINISH CREATING THIS
    #     z = 0
    #
    # def tearDown(self):
    #
# I TRIED PRINTING RETURN TO SEE WHAT IS RETURNED WHEN PROGRAM RUNS CORRECTLY.
# WHEN I DO THIS, I GET AN ERROR EVEN THOUGH THE PROGRAM WORKS
    def test_get_meme_mock_api_CHECK_returns_mock_data(self):


        print('testdata')
        print(memeFinderGiphy.get_meme("cat", True))
        print('testdata')
# I DONT THINK THIS IS WORKING CORRECTLY, BUT I AM TRYING TO TEST THE METHOD AND SEE HOW IT REACTS NORMALLY TE DETERMINE
# WHAT FORMAT OF RESPONSE I SHOULD EXPECT FROM IT.
    # # mock to replace requests.get
    # @staticmethod
    # def mock_requests_get(key):
    #     # Making a mock response as it's own class since it's it's own type of object
    #     class MockResponse:
    #         def __init__(self, json_data, status_code):
    #             self.json_data = json_data
    #             self.status_code = status_code
    #         # when json is used return json_data as it would if it were from a real api
    #
    #         def json(self):
    #             return self.json_data
    #     # 200 is standard code for url receiving data
    #     return MockResponse({"key": "data"}, 200)
    #
    # class TestGetMemeJson(unittest.TestCase):
    #
    #     # creating mock to replace requests to the url
    #     @mock.patch('requests.get', side_effect=mock_requests_get)
    #     def test_mock_request(self, mock_get):
    #         json_data = memeFinderGiphy.get_meme()
    #         self.assertEqual(json_data, {"key": "data"})


if __name__ == '__main__':
    unittest.main()