articlebot
============

Article scraping Reddit bot. Derived from @xiaoxu193's [bitofnewsbot](https://github.com/xiaoxu193/bitofnewsbot) with the significant change of scraping entire articles instead of condensing them.


How do I run it?
=====================
Setup cron to run it every minute

Instructions for Ubuntu:

* Replace username and password line in bitofnewsbot
* Install cron ``sudo apt-get install cron``
* Open up crontab to edit cron ``sudo crontab -e``
* Tell it to run every minute: ``* * * * * /usr/bin/python articlebot.py``


Submissions are stored in done.txt so they're not commented on again.

Variables
========
These are the variables you can set. 

* submissions_limit - number of top subissions to check during each cron period
* thresh_max - karma threshholds for commenting
* thresh_min - karma threshholds for commenting
* username - Reddit login details
* password - Reddit login password
* comments_per_run - comments per cron period
* sentences_per_summary - sentences per summary
* subreddits - "worldnews+worldpolitics"
* agent - "u/bitofnewsbot"
* filestore - to store submission ids of ones that are commented, "done.txt"
