import time
import json
from db_sqlite import TODAY

# Meme class object:
class Meme:
    def __init__(self, post_link="/", img_src="", source="No source", post_title="No results", keyword="", meme_only=True, date=TODAY, meme_id=''):
        self.meme_id = meme_id
        self.post_link = post_link  # post link
        self.img_src = img_src    # direct image link
        self.source = source    # where it originated from (giphy/imgur/reddit)
        self.post_title = post_title      # post title
        self.keyword = keyword
        self.meme_only = meme_only
        self.date = date    # date that's created

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)


# Holds the JSON data and other info to save within the cache
class MemeCache:
    def __init__(self, keyword, meme_only, source, data, date=TODAY):
        self.keyword = keyword
        self.meme_only = meme_only
        self.source = source
        self.data = data    # from API requeest
        self.date = date    # date that's created

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)
