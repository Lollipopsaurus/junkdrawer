# Junkdrawer
Playing around with reddit's API and bots.
The project is not meant to be serious.
The idea here is to scrape new things on reddit, send alerts based on specific criteria, and cache results to prevent repeat alerts.
I'm not responsible for anything you do with this.

# Warranty
Full text search is hard. I can't guarantee this will find the exact item you're looking for with no false positives. In fact, you'll probably get a ton of spam for things that are close or on want lists. That's better than nothing though, isn't it? If you want a system that will do that reliably, every time, find someone with hardcore regex experience that will program something up for you.

## Description

This is a simple text search app that will run every 60 seconds. The idea is to scan reddit posts, geekhack, instagram, etc. to alert you of instances of that string appearing in new posts. Discord notifications are currently working. SMS functionality through twilio will be available soonish when I stop being lazy. My end goal is a shotgun blast of notifications to alert you of items or targeted flash sales becoming available. I'm aware this could be genericized to let you scrape any reddit page for any text, but this is mainly for my personal use and a fun project, so feel free to fork it and make it something nice if you want.

The project is designed to run locally on a Linux machine, and not require any external database to function. It writes MD5 hashes of posts or status to maintain state to simple text files, and ignores those hashes it reads each time it runs. As a consequence, if pages are edited or altered, the MD5 won't match, and you'll get another hit. This can be useful for quickly changing posts, or receiving notifications of a google form being added.

I'm pretty lazy, and almost fully depend on RSS feeds to make this work. If you find bugs or anything, please let me know, and I'll fix it when I can.

### Reddit Scraper


## Instructions for use:

For real use, copy the .sample configs to the same file name without ".sample". Fill them out with your information for your bot data, etc. Some elements are hard coded, as I'm still working on how to appropriately handle large sets of inputs and types along with variants of search.

In reddit_config.cfg, you can set a JSON object of a list of targets to search for. The keys of the key/value pairs are the actual string to be searched, and the value is a qualifier to help identify what the thing is. Similar options exist for the other configuration files.

## Setup:

You need Python 3.5 or higher installed for it to work due to the discord dependencies. You can install the required libraries through Python3's pip. It's likely aliased to "pip3" if you have it.

So, run:

```
pip3 install -r requirements.txt
```

to install all the necessary libraries.

### Execution:
```
python3 discord_bot.py
```

If you'd like, you can run it in the background forever.
