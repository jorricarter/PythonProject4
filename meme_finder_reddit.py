# reddit api documentation https://www.reddit.com/dev/api/
# PRAW documentation https://praw.readthedocs.io/en/latest/

from secrets import REDDIT_ID, REDDIT_SECRET
import praw
import _thread
import logging
from praw.exceptions import APIException, ClientException, PRAWException
from classes import Meme


# logging setup
log = logging.getLogger(__name__)


def get_meme(keyword, meme_only):

    logging.info("Accessing REDDIT API")

    # create api instance
    client_id = REDDIT_ID
    client_secret = REDDIT_SECRET

    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         redirect_uri='/',
                         user_agent='testscript by /u/sz8386pr')

    # check if the reddit api login status is read-only
    logging.debug("reddit read only?:" + str(reddit.read_only))

    # if meme only check box is selected, append meme to the keyword
    if meme_only == "on":
        subreddit = 'meme'
    else:
        subreddit = 'all'

    # Checks if subreddit value is correct
    logging.debug("subreddit value: " + subreddit)

    # search parameters.
    # ToDo: In theory, query with the site: filter should work, but it doesn't work realiably. Use keyword variable instead of query for now.
    domain = 'i.redd.it'    # domain value to be used to modify query
    query = keyword + " site:" + domain  # site:i.redd.it finds submission link hosted by i.redd.it
    sort = 'relevance'    # Can be one of: relevance, hot, top, new, comments. (default: relevance).
    syntax = 'lucene'   # Can be one of: cloudsearch, lucene, plain (default: lucene).
    time_filter = 'all'     # Can be one of: all, day, hour, month, week, year (default: all).
    lim = 100      # maximum number of memes to return


    try:
        # create a memes list and if the submission url ends with the file extension
        # (In another words, 4th character from the end with a period), append the url and shortlink dictionary to the list
        # results = []
        memes = []
        submissions = reddit.subreddit(subreddit).search(keyword, sort=sort, syntax=syntax, time_filter=time_filter, limit=lim)
        for submission in submissions:
            if submission.url[-4] == '.':
                memes.append(Meme(submission.title, submission.shortlink, 'reddit', submission.url, keyword, meme_only))
                #results.append()

#        for meme in results:Meme(submission.title, submission.shortlink, 'reddit', submission.url, keyword, meme_only)
#            memes.append(create_meme_object(meme, keyword, meme_only))

        logging.info("REDDIT memes: " + str(len(memes)))

        return memes

    # http://praw.readthedocs.io/en/latest/code_overview/exceptions.html#praw.exceptions.APIException
    except APIException as e:
        logging.error(e.message)
        logging.error(e.error_type)
        logging.error(e.field)

    except ClientException or PRAWException as e:
        logging.error(e)

    # except IndexError as ie:    # when there were no
    #     logging.error(ie)
    #     return Meme('reddit')


def create_meme_object(title, shortlink, url, kw, mo):

    post_title = title   # post title
    post_link = shortlink   # reddit post link
    imc_src = url  # img src

    reddit_meme = Meme(post_link, imc_src, 'reddit', post_title, kw, mo)

    return reddit_meme




# # Enable for the command line testing
# if __name__ == "__main__":
#     keyword = input('Enter a keyword to search a meme for: ')
#     get_meme(keyword, 'on')

