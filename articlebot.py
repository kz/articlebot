import os
from os.path import join, dirname
import time
import warnings

import praw
from dotenv import load_dotenv
from newspaper import Article


# Suppress warnings
warnings.filterwarnings("ignore")

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

APP_VERSION = "v1.0.0"

BOT_NAME = os.environ.get("BOT_NAME")
AUTHOR_NAME = os.environ.get("AUTHOR_NAME")
SUBMISSIONS_LIMIT = int(os.environ.get("SUBMISSIONS_LIMIT"))  # Number of new submissions to check per run
THRESH_MIN = int(os.environ.get("THRESH_MIN"))  # Minimum karma threshold for commenting
THRESH_MAX = int(os.environ.get("THRESH_MAX"))  # Maximum karma threshold for commenting
USERNAME = os.environ.get("USERNAME")  # reddit username
PASSWORD = os.environ.get("PASSWORD")  # reddit password
COMMENTS_PER_RUN = int(os.environ.get("COMMENTS_PER_RUN"))  # Comments per cron period
SUBREDDITS = os.environ.get("SUBREDDITS")  # Subreddits to work check
LINK_STORE = os.environ.get("LINK_STORE")  # File to store IDs of crawled posts
COMMENT_STORE = os.environ.get("COMMENT_STORE")  # File to store IDs of bot comments
BLACKLIST_STORE = os.environ.get("BLACKLIST_STORE")  # File to store blacklisted URLs

USER_AGENT = "Python:" + BOT_NAME + ":" + APP_VERSION + " (by " + AUTHOR_NAME + ")"
print(USER_AGENT)


def main():
    while True:
        try:
            submissions = get_submissions()
        except praw.errors.HttpException:
            print('HTTP Exception occurred. Exiting.')
            break
        blacklist = get_blacklist()
        done = get_done()
        counts = 0  # Number of comments made this round

        for submission in submissions:
            if counts >= COMMENTS_PER_RUN:
                print("Comment count for this run reached. Exiting.")
                break
            if any(x in submission.url for x in blacklist):
                continue

            point = submission.ups - submission.downs

            if submission.id not in done and THRESH_MAX > point > THRESH_MIN:
                article = Article(submission.url)
                article.download()
                article.parse()

                if article.text.isspace():
                    print(submission.id + " does not have article text. Continuing.")
                    continue

                comment_text = form_comment(article, submission)
                while True:
                    try:
                        comment = submission.add_comment(comment_text)
                        put_comment(comment.id)
                    except praw.errors.RateLimitExceeded as error:
                        print('Rate limit exceeded. Sleeping for %d seconds. Skipping comment.' % error.sleep_time)
                        time.sleep(error.sleep_time)
                        break
                    counts += 1
                    print('Added comment for post %s - %s' % (submission.id, comment.permalink))
                    put_done(submission.id)
                    break
        break


def get_blacklist():
    with open(BLACKLIST_STORE) as f:
        return f.read().splitlines()


def get_done():
    with open(LINK_STORE) as f:
        return f.read().splitlines()


def put_done(link_id):
    with open(LINK_STORE, "a") as text_file:
        text_file.write(link_id + "\n")


def put_comment(comment_id):
    with open(COMMENT_STORE, "a") as text_file:
        text_file.write(comment_id + "\n")


def get_submissions():
    r = praw.Reddit(user_agent=USER_AGENT)
    r.login(USERNAME, PASSWORD)
    return r.get_subreddit(SUBREDDITS).get_new(limit=SUBMISSIONS_LIMIT)


def form_comment(article, submission):
    print('Forming comment for ID %s - %s - %s' % (submission.id, article.title, article.url))
    comment = "**Article title:** " + article.title + "\n"
    if article.publish_date is not None:
        comment += "\n**Publish date:** " + article.publish_date.strftime("%B %d, %Y") + "\n"
    comment += "**Article text:** \n--- \n" + article.text + "\n\n-----"
    comment += "\n^I'm ^a ^bot. ^Report ^problems [^here](http://www.reddit.com/message/compose/?to="
    comment += AUTHOR_NAME + "&subject=" + BOT_NAME + "%20enquiry&message=" + submission.url + ")^."
    return comment


if __name__ == "__main__":
    main()
