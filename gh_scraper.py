#!/usr/bin/python3
from common_junk import *
import feedparser
from bs4 import BeautifulSoup
import hashlib
import html5lib
import json
import os
import requests
from twilio.rest import Client

sms = False

def login(session, user, password):
    values = {
               "username" : user,
               "password" : password
              }

    r =  session.post("https://geekhack.org/index.php?action=login2", values)#requests.post("https://geekhack.org/index.php?PHPSESSID=se7irb0hov0nt2uolk08cuunkpfjnusu&amp;wap2", values)
    #print(r.content)
    if 'logout' in r.text:
        print('we got it')
    #print(r.text)
    return r 

def scrape_url(url, file_name):
    stored_posts = []
    if os.path.isfile(file_name):
        stored_posts = read_temp(file_name)
    session = requests.Session()
    login_stuff = login(session, '', '')
    print(session.cookies)
    print('my cookies')
    #session.auth = ('', '')
    # Scrapes reddit
    d = session.get(url)
    print(d.text) 
    to_store_posts = []
    alert_response = []
    # Looping through all of the entries we scraped
    raw_entry = soupify(d.text)
    if raw_entry:
        entry_text = raw_entry.text
        this_post_md5 = md5_post(raw_entry.text)
        to_store_posts.append(this_post_md5)
        if this_post_md5+'\n' not in stored_posts:
             data = rss_reader(raw_entry)
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

# Main that does stuff
def main():
    alert_response = scrape_url('https://geekhack.org/index.php?action=profile;area=showposts;u=53945;wap2', 'gh_100.txt')
    return alert_response
if __name__ == "__main__":
    main()
