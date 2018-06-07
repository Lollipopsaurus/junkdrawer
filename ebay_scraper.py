#!/usr/bin/python3
import feedparser
from bs4 import BeautifulSoup
import hashlib
import html5lib
import json
import os

# Uses BeautifulSoup to tease out the actual content of the post.            
def soupify(data):
    return_array = []
    soup = BeautifulSoup(data, 'html5lib')   
    divs = soup.find_all('div', class_='md')
    if len(divs) > 0:
        return divs[0]
    return ''

# Reads the file of saved md5s and returns them as an array.
def read_temp(loc):
    with open(loc, 'r') as f:
        row_array = []
        for line in f:
            row_array.append(line)
        return row_array

# Writes our md5s to disk
def write_temp(data):
    with open('ebay.txt', 'w') as f:
        for item in data:
            f.write(item+'\n')

# Encodes posts to smaller md5 strings
def md5_post(post):
    m = hashlib.md5()
    m.update(post.encode('utf-8'))
    return m.hexdigest()

# Main that does stuff
def main():
    sms = False 
    stored_posts = []
    if os.path.isfile('ebay.txt'):
        stored_posts = read_temp('ebay.txt')
    
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
                stanza = 'ETF EBAY ALERT'
                alert_response.append(stanza)
        #TODO bug here, if you don't have a raw_entry (your post is empty), you don't get written to disk. Needs to use entire post as the md5
        #else:
    write_temp(to_store_posts)
    return alert_response

if __name__ == "__main__":
    main()
