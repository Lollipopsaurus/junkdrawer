#!/usr/bin/python3
from common_junk import *
import feedparser
from bs4 import BeautifulSoup
import hashlib
import html5lib
import json
import os

hashes_file_name = 'ebay.txt'
# Main that does stuff
def main(user):
    sms = False 
    stored_posts = []
    if os.path.isfile(hashes_file_name):
        stored_posts = read_temp(hashes_file_name)
    
    # Scrapes reddit
    d = feedparser.parse('https://www.ebay.com/sch/eat_the_food/m.html?_rss=1')
    to_store_posts = []
    alert_response = []
    # Looping through all of the entries we scraped
    for entry in d.entries:
        raw_entry = soupify(entry.summary)
        if raw_entry:
            entry_text = raw_entry.text
            this_post_md5 = md5_post(raw_entry.text)
            to_store_posts.append(this_post_md5)
            if this_post_md5 not in stored_posts:
                stanza = 'ETF EBAY ALERT + https://www.ebay.com/sch/eat_the_food/m.html?_nkw=&_armrs=1&_ipg=&_from='
                alert_response.append(stanza)
        #TODO bug here, if you don't have a raw_entry (your post is empty), you don't get written to disk. Needs to use entire post as the md5
        #else:
    write_temp(to_store_posts, 'user_data/' + user['name'] + '/' + hashes_file_name)
    return alert_response

if __name__ == "__main__":
    main()
