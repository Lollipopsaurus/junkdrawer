#!/usr/bin/python3
from common_junk import *
import feedparser
from bs4 import BeautifulSoup
import requests
import hashlib
import html5lib
import json
import re
import os
from twilio.rest import Client

sms = False
configs = {}

def scrape_op_url(url, file_name, message):
    stored_posts = []
    d = None
    if os.path.isfile(file_name):
        stored_posts = read_temp(file_name)
    try:
        d = requests.get(url)
    except Exception as e:
       print(e)
       return
    to_store_posts = []
    alert_response = set()
    # Looping through all of the entries we scraped
    soup = BeautifulSoup(d.text, 'html.parser')
    etf_main_post = soup.findAll('script')
    if etf_main_post:
        try:
            json_string = etf_main_post[3].string[21:][:-1]
            json_string = json.loads(json_string)
        except Exception as e:
            #print("found error parson json from instagram")
            #print(json.loads(etf_main_post[3].string[17:][:-1])['description'])
            json_string = json.loads(etf_main_post[3].string[17:][:-1])

        if 'entry_data' in json_string:
            if json_string['entry_data']['ProfilePage'][0]['graphql']['user']['external_url']:
                json_string = json_string['entry_data']['ProfilePage'][0]['graphql']['user']['external_url']
            elif json_string['entry_data']['ProfilePage'][0]['graphql']['user']['biography']:
                json_string = json_string['entry_data']['ProfilePage'][0]['graphql']['user']['biography']
        elif 'description' in json_string:
            #print(json_string)
            json_string = json_string['description'] 

        this_post_md5 = md5_post(json_string)
        to_store_posts.append(this_post_md5)
        if this_post_md5+'\n' not in stored_posts and len(stored_posts) > 0:
            alert_response.add(message + ' ' + json_string)
    write_temp(to_store_posts, file_name)
    return alert_response

# Main that does stuff
def main(user):
    configs = user['reddit_cfg']
    username = user['name']
    user_id = user['discord_id']
    targets = {}

    alert_response = scrape_op_url('https://www.instagram.com/nightcaps.keycaps/', 'user_data/nightcapsinsta.txt', '<@&' + user['discord_role_id'] + '> ETF Insta profile change')
    alert_response = alert_response.union(scrape_op_url('https://www.instagram.com/gaf_caps/', 'user_data/gafinsta.txt', '<@&' + user['discord_role_id'] + '> GAF Insta profile change'))
    return alert_response
if __name__ == "__main__":
    main()
