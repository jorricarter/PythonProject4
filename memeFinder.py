class Meme:
    def __init__(self, source, title, img_src, post_link):
        self.source = source    # where it originated from (giphy/imgur/reddit)
        self.title = title      # post title
        self.img_src = img_src    # direct image link
        self.post_link = post_link  # post link
