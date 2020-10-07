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

def scrape_rss_posts(rss_url, file_name, configs):
    stored_posts = []
    targets = configs['reddit_cfg']['targets']
    report = True
    if os.path.isfile(file_name):
        stored_posts = read_temp(file_name)

    # Scrapes reddit
    d = feedparser.parse(rss_url)
    to_store_posts = []
    alert_response = set()

    # Looping through all of the entries we scraped
    for entry in d.entries:
        raw_entry = soupify(entry.summary)
        if raw_entry:
            entry_text = raw_entry.text.lower()
            this_post_md5 = md5_post(raw_entry.text)
            to_store_posts.append(this_post_md5)
            if this_post_md5+'\n' not in stored_posts and len(stored_posts) > 0:
                match = False
                for target in targets.items():
                    if isinstance(target[1], str):
                        if target[1].lower() in entry.title.lower() or target[1].lower() in entry_text:
                            match = target[1]
                    else:
                        this_match = target[1].match(entry.title) or target[1].match(entry_text)
                        if this_match:
                            match = this_match.group()
                if match and '/u/' + configs['reddit_cfg']['reddit_id'] != entry.author:
                    stanza = '<@' + configs['discord_id'] + '> ' + match + ' found! link: ' + entry.link
                    alert_response.add(stanza)

        #TODO bug here, if you don't have a raw_entry (your post is empty), you don't get written to disk. Needs to use entire post as the md5
        #else:
    write_temp(to_store_posts, file_name)
    return alert_response

def scrape_reddit_user(reddit_url, file_name, user_id, message):
    stored_posts = []
    if os.path.isfile(file_name):
        stored_posts = read_temp(file_name)

    d = feedparser.parse(reddit_url) 
    to_store_posts = []
    alert_response = set()

    # Looping through all of the entries we scraped
    for entry in d.entries:
        raw_entry = soupify(entry.summary)
        if raw_entry:
            entry_text = raw_entry.text
            this_post_md5 = md5_post(raw_entry.text)
            to_store_posts.append(this_post_md5)
            if this_post_md5+'\n' not in stored_posts and len(stored_posts) > 0:
                stanza = message + ' ' + entry.link + ' '
                form_link = entry_text.find('http')
                if form_link != -1:
                    linkaroo = entry_text[form_link: form_link + 150]
                    stanza += 'link to form: ' + linkaroo
                alert_response.add(stanza)
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

    #for target in configs['targets'].items():
    #    if target[1].startswith('^'):
    #        targets[target[0]] = re.compile(target[1], re.IGNORECASE)
    #    else:
    #        targets[target[0]] = target[1]

    #configs['targets'] = targets

    alert_response = scrape_rss_posts('https://www.reddit.com/r/mechmarket/new/.rss?sort=new&limit=100', 'user_data/' + username + '/mech_100.txt', user)
    alert_response = alert_response.union(scrape_reddit_user('http://www.reddit.com/user/eat_the_food/submitted/.rss', 'user_data/mamcus_reddit.txt', user_id, '<@&' + user['discord_role_id'] + '> Possible ETF activity on reddit'))
    alert_response = alert_response.union(scrape_reddit_user('http://www.reddit.com/user/poptart_777/submitted/.rss', 'user_data/poptart_reddit.txt', user_id, '<@&690765849036062761> Possible Switchnollie activity on reddit'))
    alert_response = alert_response.union(scrape_reddit_user('http://www.reddit.com/user/otanishock/submitted/.rss', 'user_data/otani_reddit.txt', user_id, '<@&690765849036062761> Possible otanishock sellout activity on reddit'))
    #if 'Lollipopsaurus' == username:
    #    alert_response = alert_response.union(scrape_rss_posts('https://www.reddit.com/r/watchexchange/new/.rss?sort=new&limit=100', 'user_data/' + username + '/watch_100.txt', user))
    return alert_response
if __name__ == "__main__":
    main()
