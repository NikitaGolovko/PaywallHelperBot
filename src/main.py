import praw
from datetime import datetime, timedelta

BOT_NAME = "PaywallHelperBot"
SUBREDDITS = ["Maine", "portlandme"]
QUESTIONS = ["what is", "who is", "what are"]
REPLY_TEMPLATE = "[Link](https://12ft.io/{}) for those who need help getting over a paywall"
DOMAIN_LISTINGS = ["pressherald.com", "bangordailynews.com"]
HOURS_OFFSET = 24

def main():
    reddit = praw.Reddit(
        user_agent="PaywallHelperBot (by u/PaywallHelperBot)",
        client_id="",
        client_secret="",
        username="PaywallHelperBot",
        password="",
    )

    print(reddit.user.me())

    offset_time =  datetime.utcnow() - timedelta(hours=HOURS_OFFSET)
    unix_timestamp_offset_time = datetime.timestamp(offset_time)*1000
    for subredditName in SUBREDDITS:
        subreddit = reddit.subreddit(subredditName)
        for submission in subreddit.new():
    #    for submission in subreddit.stream.submissions():
            if submission.created_utc > unix_timestamp_offset_time:
                print(submission.title) 
                process_submission(submission)

    print("Done processing")


def delete_comment(comment):
    print(f"Deleting a comment: {comment.body}")
    comment.delete()
    

def process_submission(submission):
    for domain in DOMAIN_LISTINGS:
        if domain in submission.url:
            print(submission.title)
            print(submission.url)
            if not already_responded(submission):
                reply_text = REPLY_TEMPLATE.format(submission.url)
                print(reply_text)
                #submission.reply(reply_text)


def already_responded(submission):
    for comment in submission.comments:
        if comment.author.name == BOT_NAME:
            print(comment.body)
            return True
    
    return False

if __name__ == "__main__":
    main()