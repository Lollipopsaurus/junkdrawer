import errno
import feedparser
from bs4 import BeautifulSoup
import hashlib
import html5lib
import json
import os
from twilio.rest import Client

# This guy reads the rss, and finds the posts with the targets listed.
def rss_reader(content, targets):
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
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, 'w') as f:
        for item in data:
            f.write(item+'\n')

# Encodes posts to smaller md5 strings
def md5_post(post):
    m = hashlib.md5()
    m.update(post.encode('utf-8'))
    return m.hexdigest()
