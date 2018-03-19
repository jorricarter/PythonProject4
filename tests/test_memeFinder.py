import memeFinder
from unittest import TestCase
from unittest.mock import patch
from memeFinder import Meme


class TestMemeFinderModule(TestCase):

    # this function removes en/decoding issues occurs during loading from/to webpage
    #   &#39;, &#34;, or \xa0 are improperly converted due to en/decoding issue
    def test_fix_annoying_amps(self):
        # create some temp Meme objects
        quote_meme = Meme('source')
        blank_meme = Meme('source')
        quote_meme.title = '&#34;Tester&#39;s agony&#34;'
        blank_meme.title = '\xa0'

        fixed_quote_meme = memeFinder.fix_annoying_amps([quote_meme])
        fixed_blank_meme = memeFinder.fix_annoying_amps([blank_meme])

        # fix_annoying_amps will fix the ASCII codes into proper strings " or '
        self.assertEqual(fixed_quote_meme[0].title, '"Tester\'s agony"')
        # if title was blank or \xa0, should be defaulted to 'NO TITLE'
        self.assertEqual(fixed_blank_meme[0].title, 'NO TITLE')