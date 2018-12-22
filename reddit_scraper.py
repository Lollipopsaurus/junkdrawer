#!/usr/bin/python3
from common_junk import *
import feedparser
from bs4 import BeautifulSoup
import hashlib
import html5lib
import json
import re
import os
from twilio.rest import Client

sms = False
configs = {}

def scrape_rss_posts(rss_url, file_name, configs, username, user_id):
    stored_posts = []
    targets = configs['targets']
    report = True
    if os.path.isfile(file_name):
        stored_posts = read_temp(file_name)
    # else:
    #     report = False

    # Scrapes reddit
    d = feedparser.parse(rss_url)
    to_store_posts = []
    alert_response = []

    # Looping through all of the entries we scraped
    for entry in d.entries:
        raw_entry = soupify(entry.summary)
        if raw_entry:
            entry_text = raw_entry.text
            this_post_md5 = md5_post(raw_entry.text)
            to_store_posts.append(this_post_md5)
            if this_post_md5+'\n' not in stored_posts:
                match = False

                for target in targets.items():
                    if isinstance(target[1], str):
                        if target[1] in entry.title.lower() or target[1] in entry.summary.lower():
                            match = target[1]
                    else:
                        this_match = target[1].match(entry.title) or target[1].match(entry.summary)
                        if this_match:
                            match = this_match.group()

                if match:
                    stanza = '<@' + user_id + '> ' + match + ' found! link: ' + entry.link
                    if sms:
                        #sms(stanza)
                        print('entry')
                    if report:
                        alert_response.append(stanza)

        #TODO bug here, if you don't have a raw_entry (your post is empty), you don't get written to disk. Needs to use entire post as the md5
        #else:
    write_temp(to_store_posts, file_name)
    return alert_response

def scrape_reddit_user(user, file_name, user_id):
    stored_posts = []
    if os.path.isfile(file_name):
        stored_posts = read_temp(file_name)

    d = feedparser.parse(user) 
    to_store_posts = []
    alert_response = []

    # Looping through all of the entries we scraped
    for entry in d.entries:
        raw_entry = soupify(entry.summary)
        if raw_entry:
            entry_text = raw_entry.text
            this_post_md5 = md5_post(raw_entry.text)
            to_store_posts.append(this_post_md5)
            if this_post_md5+'\n' not in stored_posts:
                stanza = 'Possible ETF activity on reddit'
                if sms:
                    #sms(stanza)
                    print('entry')
                alert_response.append(stanza)
        #TODO bug here, if you don't have a raw_entry (your post is empty), you don't get written to disk. Needs to use entire post as the md5
        #else:
    write_temp(to_store_posts, file_name)
    return alert_response

# Main that does stuff
def main(user):
    configs = user['reddit_cfg']
    username = user['name']
    user_id = user['discord_id']
    targets = {}

    for target in configs['targets'].items():
        if target[1].startswith('^'):
            targets[target[0]] = re.compile(target[1], re.IGNORECASE)
        else:
            targets[target[0]] = target[1]

    configs['targets'] = targets

    alert_response = scrape_rss_posts('https://www.reddit.com/r/mechmarket/new/.rss?sort=new&limit=100', 'user_data/' + username + '/mech_100.txt', configs, username, user_id)
    alert_response += scrape_reddit_user('http://www.reddit.com/user/eat_the_food/.rss', 'user_data/mamcus.txt', user_id)
    return alert_response
if __name__ == "__main__":
    main()
