import os
from os.path import join, dirname

import praw
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

APP_VERSION = "v1.0.0"

BOT_NAME = os.environ.get("BOT_NAME")
AUTHOR_NAME = os.environ.get("AUTHOR_NAME")
SUBMISSIONS_LIMIT = os.environ.get("SUBMISSIONS_LIMIT")  # Number of new submissions to check during each cron period
THRESH_MIN = os.environ.get("THRESH_MIN")  # Minimum karma threshold for commenting
THRESH_MAX = os.environ.get("THRESH_MAX")  # Maximum karma threshold for commenting
USERNAME = os.environ.get("USERNAME")  # reddit username
PASSWORD = os.environ.get("PASSWORD")  # reddit password
COMMENTS_PER_RUN = os.environ.get("COMMENTS_PER_RUN")  # Comments per cron period
SUBREDDITS = os.environ.get("SUBREDDITS")  # Subreddits to work check
FILESTORE = os.environ.get("FILESTORE")  # File to store submission ids of ones that are commented

USER_AGENT = "Python:" + BOT_NAME + ":" + APP_VERSION + " (by " + AUTHOR_NAME + ")"


def main():
    submissions = getSubmissions()
    done = getDone()
    counts = 0  # how many comments made this round

    for submission in submissions:
        if counts >= COMMENTS_PER_RUN:
            break
        id = submission.id
        point = submission.ups - submission.downs

        if id not in done and THRESH_MAX > point > THRESH_MIN:
            putDone(submission.id)
            sentences = pyteaser.SummarizeUrl(submission.url)
            if sentences is not None:
                counts += 1
                comment = formComment(sentences, submission)

            submission.add_comment(comment)
            print(comment)


def getDone():
    with open(FILESTORE) as f:
        return f.read().splitlines()


def putDone(id):
    with open(FILESTORE, "a") as text_file:
        text_file.write(id + "\n")


def getSubmissions():
    r = praw.Reddit(user_agent=USER_AGENT)
    r.login(USERNAME, PASSWORD)
    return r.get_subreddit(SUBREDDITS).get_new(limit=SUBMISSIONS_LIMIT)


def formComment(sentences, submission):
    print(submission.title + ": " + submission.url)

    point = submission.ups - submission.downs
    comment = "**Article summary:** \n"
    count = 0
    if sentences is None or len(sentences) < 3:
        return None
    for sentence in sentences:
        if count < SENTENCES_PER_SUMMARY:
            sentence.replace('\n', ' ')
            comment += ("\n>* " + sentence + "\n")
            count += 1
    comment += "\n^I'm ^a ^bot, ^v2. ^Report ^problems [^here](http://reddit.com/r/bitofnewsbot). \n\n**^Learn ^how ^it ^works: [^Bit ^of ^News](http://www.bitofnews.com/about.html)**"
    return comment


if __name__ == "__main__":
    main()
