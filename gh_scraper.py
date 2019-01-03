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

def scrape_op_url(url, file_name, message):
    stored_posts = []
    d = None 
    if os.path.isfile(file_name):
        stored_posts = read_temp(file_name)
    #try: 
    d = requests.get(url)
    #except Exception as e:
    #   pass 
    to_store_posts = []
    alert_response = []
    # Looping through all of the entries we scraped
    soup = BeautifulSoup(d.text, 'html.parser')
    etf_main_post = soup.find('div', attrs={'class':'inner', 'id':'msg_2048390'})
    if etf_main_post:
        this_post_md5 = md5_post(etf_main_post.text)
        to_store_posts.append(this_post_md5)
        if this_post_md5+'\n' not in stored_posts and len(stored_posts) > 0:
            alert_response.append(message + url + ' ' + etf_main_post.text)
    write_temp(to_store_posts, file_name)
    return alert_response

def scrape_clack_happens_url(url, file_name, message):
    stored_posts = []
    if os.path.isfile(file_name):
        stored_posts = read_temp(file_name)
    #try:
    d = requests.get(url)
    #except Exception as e:
    #    pass
    to_store_posts = []
    alert_response = []

    soup = BeautifulSoup(d.text, 'html.parser')
    clack_thread = soup.find_all('div', attrs={'class':'post_wrapper'})

    for post in clack_thread:
        soup2 = BeautifulSoup(str(post), 'html.parser')
        clack_happens_post = soup2.find('div', attrs={'class':'inner'})
        this_post_md5 = md5_post(clack_happens_post.text)
        if 'Clack Happens #' in clack_happens_post.text:
            to_store_posts.append(this_post_md5)
            if this_post_md5+'\n' not in stored_posts and len(stored_posts) > 0:
                alert_response.append(message + url + ' Text:' + clack_happens_post.text + ' Refresh here until you can post >>>>>>>>>>>>>>>>>>>> https://geekhack.org/index.php?action=post;topic=98411.0 <<<<<<<<<<<<<<<<<<<<< Press f5 until you can post you dumb motherfucker' )

    write_temp(to_store_posts, file_name)
    return alert_response

# Main that does stuff
def main(user):
    alert_response = scrape_op_url('https://geekhack.org/index.php?topic=79513.msg2048390#msg2048390', 'user_data/gh_etf.txt', '<@&' + user['discord_role_id'] + '> ETF EDIT ON GH ')
    alert_response += scrape_clack_happens_url('https://geekhack.org/index.php?topic=98411.10000000', 'user_data/gh_clackhappens.txt', '<@&' + user['discord_role_id'] + '> CLACK HAPPENS ON GH ')
    return alert_response
if __name__ == "__main__":
    main()
