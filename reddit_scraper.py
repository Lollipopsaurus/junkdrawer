#!/usr/bin/python3
from common_junk import *
import feedparser
from bs4 import BeautifulSoup
import hashlib
import html5lib
import json
import os
from twilio.rest import Client

sms = False
configs = {}
"""
#TODO Deprecating this for now. Still works, but meh, discord is better/cheaper.
def sms(content):

# Find these values at https://twilio.com/user/account
    print(sys.argv[1])
    account_sid = sys.argv[1] 
    auth_token = sys.argv[2]
    to_phone = sys.argv[3]
    from_phone = sys.argv[4]

    client = Client(account_sid, auth_token)

    client.api.account.messages.create(
        to="+1" + to_phone,
        from_="+1" + from_phone,
        body="Found on mechmarket! " + content)
#TODO
def user_rss():
    print('test')

#Finds target random words
def line_mod(line, target, variant):
    mod = ''
    if 'bk' in line or 'bombking' in line or 'bomb king' in line:
        if variant in line:
            mod = 'Found ' + target + ' ' + variant
        else:
            mod = 'Found ' + target + '. Cannot confirm variant'
    elif 'fugu' in line:
        mod = 'Found ' + target + ' fugu'
    elif 'keybuto' in line:
        mod = 'Found ' + target + 'keybuto'
    line = mod
    return line
"""
def scrape_rss_posts(rss_url, file_name, configs):
    stored_posts = []
    targets = configs['targets']
    if os.path.isfile(file_name):
        stored_posts = read_temp(file_name)

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
                data = rss_reader(entry_text, targets)
                for item in data:
                    for target in targets:
                        if target in item:
                            stanza = item + ' found, it could be a ' + targets[item] + ' link:' + entry.link
                            if sms:
                                #sms(stanza)
                                print('entry')
                            alert_response.append(stanza)
        #TODO bug here, if you don't have a raw_entry (your post is empty), you don't get written to disk. Needs to use entire post as the md5
        #else:
    write_temp(to_store_posts, file_name)
    return alert_response

def scrape_reddit_user(user, file_name):
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
                stanza = 'ETF ON REDDIT'
                if sms:
                    #sms(stanza)
                    print('entry')
                alert_response.append(stanza)
        #TODO bug here, if you don't have a raw_entry (your post is empty), you don't get written to disk. Needs to use entire post as the md5
        #else:
    write_temp(to_store_posts, file_name)
    return alert_response

# Main that does stuff
def main():
    with open('reddit_config.cfg', 'r') as config_raw:
        configs = json.load(config_raw)
        alert_response = scrape_rss_posts('https://www.reddit.com/r/mechmarket/new/.rss?sort=new&limit=100', 'mech_100.txt', configs)
        alert_response += scrape_reddit_user('http://www.reddit.com/user/eat_the_food/.rss', 'mamcus.txt')
        return alert_response
if __name__ == "__main__":
    main()
