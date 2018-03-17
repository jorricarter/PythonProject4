import memeFinderGiphy
import unittest
import os
from unittest import TestCase
from unittest import mock
from unittest.mock import Mock
from unittest.mock import patch


class TestGetMeme(unittest.TestCase):

    # def setUp(self):
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
