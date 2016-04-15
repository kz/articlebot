articlebot
============

Article scraping Reddit bot. Derived from xiaoxu193's [bitofnewsbot](https://github.com/xiaoxu193/bitofnewsbot) with the significant change of scraping entire articles instead of condensing them.

You can find an example of articlebot in use by [/u/justice_article_bot](http://www.reddit.com/user/justice_article_bot).

How do I run it?
=====================
Setup cron to run it every minute

Instructions for Ubuntu:

* Install dependencies
* Rename ``.env.example`` to ``.env`` and edit accordingly
* Rename ``blacklist.txt.example``, ``comments.txt.example`` and ``links.txt.example`` to ``*.txt`` accordingly
* Install cron ``sudo apt-get install cron``
* Open up crontab to edit cron ``sudo crontab -e``
* Tell it to run every minute: ``* * * * * /usr/bin/python articlebot.py``

``done.txt`` and ``comments.txt`` prevent duplicate comments. ``blacklist.txt`` causes bots to ignore listed sites.

Dependencies:

* [praw](https://github.com/praw-dev/praw)
* [python-dotenv](https://github.com/theskumar/python-dotenv)
* [newspaper](https://github.com/codelucas/newspaper)
* [py-pretty](https://pypi.python.org/pypi/py-pretty)
