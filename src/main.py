import praw
from datetime import datetime, timedelta, timezone

BOT_NAME = "PaywallHelperBotv2"
SUBREDDITS = ["Maine", "portlandme"]
QUESTIONS = ["what is", "who is", "what are"]
REPLY_TEMPLATE = "[Link](https://12ft.io/proxy?q={}) for those who need help getting over a paywall"
HOURS_OFFSET = 48
OFFSET_TIME_FOR_SEARCHING = (datetime.now(timezone.utc) - timedelta(hours=HOURS_OFFSET)).timestamp()
OFFSET_TIME_FOR_RESPONDING = (datetime.now(timezone.utc) - timedelta(hours=6)).timestamp()
LOG_FILE = './'

def main():
    reddit = praw.Reddit(
        user_agent="PaywallHelperBotv2 (by u/PaywallHelperBotv2)",
        client_id="",
        client_secret="",
        username="PaywallHelperBotv2",
        password="",
    )

    logToFile('Start', 'Starting the bot')

    #print(reddit.user.me())

    for subredditName in SUBREDDITS:
        subreddit = reddit.subreddit(subredditName)
        for submission in subreddit.new():
                print(submission.title) 
                print(datetime.fromtimestamp(submission.created_utc))
                process_submission(submission)

    logToFile('End', 'Done processing!')



def delete_comment(comment):
    print(f"Deleting a comment: {comment.body}")
    comment.delete()
    

def process_submission(submission):
    if submission.created_utc > OFFSET_TIME_FOR_SEARCHING:
    for domain in DOMAIN_LISTINGS:
        if domain in submission.url:
            if not already_responded(submission):
                    submission.upvote()
                    if (submission.created_utc > OFFSET_TIME_FOR_RESPONDING): 
                reply_text = REPLY_TEMPLATE.format(submission.url)
                        logToFile('PreparedResponse', 'Post: {postTitle}, URL: {postURL}, Response: {postResponse}'.format(postTitle=submission.title, postURL=submission.shortlink, postResponse=reply_text))
                        submission.reply(reply_text)


def already_responded(submission):
    for comment in submission.comments:
        if comment.author.name == BOT_NAME:
            return True
    
    return False

def logToFile(title, message): 
    f = open(BOT_NAME+".txt", "a")
    f.write('{date:%Y-%m-%d_%H:%M:%S}, {title}, {message}\n'.format(date=datetime.now(), title=title, message=message))
    f.close()

if __name__ == "__main__":
    main()