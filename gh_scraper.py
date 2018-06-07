#!/usr/bin/python3
import feedparser
from bs4 import BeautifulSoup
import hashlib
import html5lib
import json
import os
import requests
from twilio.rest import Client

sms = False

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
# This guy reads the rss, and finds the posts with the targets listed.
def rss_reader(entry):
    content = entry.text
    found = []
    # Loop through targets
    for target in targets.keys():
        # If target is in content
        if target.lower() in content.lower():
            # Check if target is in last 50 records
            found.append(target)
    return found

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
def write_temp(data, file_name):
    with open(file_name, 'w') as f:
        for item in data:
            f.write(item+'\n')

# Encodes posts to smaller md5 strings
def md5_post(post):
    m = hashlib.md5()
    m.update(post.encode('utf-8'))
    return m.hexdigest()

def scrape_url(url, file_name):
    stored_posts = []
    if os.path.isfile(file_name):
        stored_posts = read_temp(file_name)

    # Scrapes reddit
    d = requests.get(url) 
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
