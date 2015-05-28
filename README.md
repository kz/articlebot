articlebot
============

Article scraping Reddit bot. Derived from xiaoxu193's [bitofnewsbot](https://github.com/xiaoxu193/bitofnewsbot) with the significant change of scraping entire articles instead of condensing them.


How do I run it?
=====================
Setup cron to run it every minute

Instructions for Ubuntu:

* Install dependencies
* Rename ``.env.example`` to ``.env`` and edit accordingly
* Install cron ``sudo apt-get install cron``
* Open up crontab to edit cron ``sudo crontab -e``
* Tell it to run every minute: ``* * * * * /usr/bin/python articlebot.py``

Submissions are stored in done.txt so they're not commented on again.

Dependencies:

* [praw](https://github.com/praw-dev/praw)
* [python-dotenv](https://github.com/theskumar/python-dotenv)
* [newspaper](https://github.com/codelucas/newspaper)
* [py-pretty](https://pypi.python.org/pypi/py-pretty)