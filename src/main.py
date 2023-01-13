import praw
from datetime import datetime, timedelta, timezone
from Handlers.paywallHandler import *
import logging
import logging.config
import re
import os
from os import path
from distutils.util import strtobool
from dotenv import load_dotenv

# Initialize .env file
load_dotenv()

BOT_NAME = 'PaywallHelperBotv2'
SUBREDDITS = ['Maine', 'portlandme']
REPLY_TEMPLATE = '[Link]({}) for those who need help getting over a paywall'
DOMAIN_LISTINGS = ['pressherald.com', 'bangordailynews.com',
                   'spectrumlocalnews.com', 'centralmaine.com']
HOURS_OFFSET = 48
OFFSET_TIME_FOR_SEARCHING = (datetime.now(
    timezone.utc) - timedelta(hours=HOURS_OFFSET)).timestamp()
OFFSET_TIME_FOR_RESPONDING = (datetime.now(
    timezone.utc) - timedelta(hours=6)).timestamp()
LOG_FILE = './'
# will eventually move this to be an argument (or config value)
EMULATE_DISPLAY = bool(strtobool(os.environ.get("EMULATE_DISPLAY", 'False')))


# Init logging for my app
logging.config.fileConfig(
    path.join(path.dirname(path.abspath(__file__)), 'logging.conf'))
# create logger
logger = logging.getLogger(BOT_NAME)
logging.basicConfig()


def main():
    logger.info('Starting this all!')

    reddit = praw.Reddit(
        user_agent='PaywallHelperBotv2 (by u/PaywallHelperBotv2)',
        client_id=os.environ.get("REDDIT_CLIENT_ID"),
        client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
        username="PaywallHelperBotv2",
        password=os.environ.get("REDDIT_PASSWORD"),
    )

    logger.debug('Bot init completed!')

    for subredditName in SUBREDDITS:
        subreddit = reddit.subreddit(subredditName)
        for submission in subreddit.new():
            logger.debug(f'{submission.created_utc} - {submission.title}')
            process_submission(submission)

    logger.info('End of processing')


def process_submission(submission):
    if submission.created_utc > OFFSET_TIME_FOR_SEARCHING:
        for domain in DOMAIN_LISTINGS:
            if domain in submission.url:
                if not already_responded(submission):
                    submission.upvote()
                    if (submission.created_utc > OFFSET_TIME_FOR_RESPONDING):
                        try:
                            handler = PaywallHandler(EMULATE_DISPLAY)
                            processedURL = handler.submit_url(
                                extract_url(submission.url))
                            reply_text = REPLY_TEMPLATE.format(processedURL)
                            logger.info('Post: {postTitle}, URL: {postURL}, Response: {postResponse}'.format(
                                postTitle=submission.title, postURL=submission.shortlink, postResponse=reply_text))
                            submission.reply(reply_text)
                        except WorkInProgressException as ex_wip:
                            logger.info(
                                f'Work in progress encountered!. {ex_wip.currentURL}')
                        except Exception as ex_generic:
                            logger.error(
                                f'Something failed while handling response! Ex: {ex_generic}')


def already_responded(submission):
    for comment in submission.comments:
        if comment.author.name == BOT_NAME:
            return True

    return False


def extract_url(text):
    url_regex = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    match = re.search(url_regex, text)
    if match:
        return match.group()
    return None


if __name__ == '__main__':
    main()
