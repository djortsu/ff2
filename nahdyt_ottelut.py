from bs4 import BeautifulSoup
from collections import OrderedDict
import os
import requests
import sys
import time

def get_page_count(input_page):
    response = requests.get(input_page)
    if response.status_code != 200:
        print("NYT YLLAPITO PAIKALLE! OLENKO ULKOMAILLA?")
        sys.exit(1)
    soup = BeautifulSoup(response.content.decode('iso-8859-1'), 'html.parser')
    for y1 in soup.find_all('div', class_='middletext wordspacing'):
        if "Sivuja: [" in y1.get_text():
            if y1.get_text()[-2] == "]":
                return 1
            else:
                return int(y1.get_text().split(" ")[-2])

def parse_page(input_page, i):
    page_index = i*25
    response = requests.get(input_page + "." + str(page_index))
    soup = BeautifulSoup(response.content.decode('iso-8859-1'), 'html.parser')

    topic = input_page.split("=")[1].split(".")[0]
    
    nick_link_dict = {}
    nicks = []
    links = []
    for x1 in soup.find_all('a'):
        x2 = x1.get('title')
        if x2 is not None:
            if "Tarkastele profiilia" in x2:
                nicks.append(x1.string)
    for y1 in soup.find_all('div'):
        if y1.get('class') == ['saihe']:
            id = y1.get('id').split("_")[1]
            links.append(input_page.split("=")[0] + "=" + topic + ".msg" + id + "#msg" + id)
    
    del nicks[::2]
    nick_link_dict = {nicks[i]: links[i] for i in range(len(nicks))}

    return nick_link_dict

def make_post_content(dict):
    post_content = ""
    post_list = []
    for key in list(dict):
        search_string = "[b]" + key[0].upper()
        add_new = True
        for i in range(len(post_list)):
            if search_string in post_list[i]:
                replace_string = post_list[i] + ", [url=" + dict[key] + "]" + key + "[/url]"
                post_list[i] = replace_string
                add_new = False
        if add_new:
            post_list.append("[b]" + key[0].upper() + "[/b] - [url=" + dict[key] + "]" + key + "[/url]")

    for item in post_list:
        post_content += item
        post_content += "\n"
    
    return post_content

def post_post(input_page, msg_content, msg_num, user, passwd):
    with requests.Session() as s:
        login_url = "https://futisforum2.org/index.php?action=login2"
        login_response = s.post(login_url, data={"user": user, "passwrd": passwd})
        if login_response.status_code != 200:
            print("NYT YLLAPITO PAIKALLE! OLENKO ULKOMAILLA?")
            sys.exit(1)
        time.sleep(1)
        r1 = s.get(input_page)
        soup1 = BeautifulSoup(r1.content.decode('iso-8859-1'), 'html.parser')
        all_a = soup1.find_all('a')
        edit_link = ""
        for item in all_a:
            i_href = item.get('href')
            if i_href is not None:
                if f"action=post;msg={msg_num}" in i_href:
                    edit_link = i_href
        if edit_link == "":
            print("MODET JUMALAUTA! OLENKO BANNISSA?")
            sys.exit(1)
        time.sleep(1)
        r2 = s.get(edit_link)
        soup2 = BeautifulSoup(r2.content.decode('iso-8859-1'), 'html.parser')
        forms = soup2.find_all('form', id='postmodify')
        action_link = forms[0].get('action')
        inputs = forms[0].find_all('input')
        for i in inputs:
            if i['name'] == "subject":
                subject = i['value'].encode("ISO-8859-1")
            elif i['name'] == "num_replies":
                num_replies = i['value']
            elif i['name'] == "additional_options":
                additional_options = i['value']
            elif i['name'] == "sc":
                sc = i['value']
            elif i['name'] == "seqnum":
                seqnum = i['value']
        icon = "xx"
        goback = "1"
        post = "Tallenna"
        topic = input_page.split("=")[-1]
        message = msg_content.encode("ISO-8859-1")
        post_data={"topic": topic, "subject": subject, "icon": icon, "message": message, "goback": goback, "post": post, "num_replies": num_replies, "additional_options": additional_options, "sc": sc, "seqnum": seqnum}
        for key in post_data:
            if post_data[key] == "":
                print("EIKO TAIDOT RIITA!?")
                sys.exit(1)
        time.sleep(1)
        post_response = s.post(action_link, data=post_data)

#############################################################

hot_topic = "https://futisforum2.org/index.php?topic=282555"
hot_msg = "17139587"
hot_user = "nahdytottelut"
hot_pw = os.getenv("HOT_PW")

print("Getting page count...")
page_count = get_page_count(hot_topic)
time.sleep(1)

full_nick_link_dict = {}

for i in range(page_count):
    print(f"Parsing page {i+1}...")
    nick_link_dict = parse_page(hot_topic, i)
    time.sleep(1)
    if i == 0:
        del nick_link_dict[next(iter(nick_link_dict))]
    full_nick_link_dict.update(nick_link_dict)

sorted_nick_link_dict = OrderedDict(sorted(full_nick_link_dict.items(), key=lambda x: x[0].lower()))

post_content = make_post_content(sorted_nick_link_dict)
post_content += "\n" + "Foorumisteja: " + str(len(sorted_nick_link_dict)) + "\n"
post_content += "\n" + "Vanhat:" + "\n"
post_content += "[url=https://futisforum2.org/index.php?topic=276317]2025[/url], [url=http://futisforum2.org/index.php?topic=269927]2024[/url], [url=http://futisforum2.org/index.php?topic=263126]2023[/url], [url=http://futisforum2.org/index.php?topic=254623]2022[/url], [url=http://futisforum2.org/index.php?topic=242684]2021[/url], [url=http://futisforum2.org/index.php?topic=234715]2020[/url], [url=http://futisforum2.org/index.php?topic=224630]2019[/url], [url=http://futisforum2.org/index.php?topic=214095]2018[/url], [url=http://futisforum2.org/index.php?topic=203315]2017[/url], [url=http://futisforum2.org/index.php?topic=190345]2016[/url], [url=http://futisforum2.org/index.php?topic=178127]2015[/url], [url=http://futisforum2.org/index.php?topic=163350]2014[/url], [url=http://futisforum2.org/index.php?topic=150525]2013[/url], [url=http://futisforum2.org/index.php?topic=133276]2012[/url], [url=http://futisforum2.org/index.php?topic=114936]2011[/url], [url=http://futisforum2.org/index.php?topic=92118]2010[/url], [url=http://futisforum2.org/index.php?topic=63884]2009[/url], [url=http://futisforum2.org/index.php?topic=42920]2008[/url], [url=http://futisforum2.org/index.php?topic=10358]2007[/url], [url=http://futisforum2.org/index.php?topic=1109]2006[/url]"
#post_content += "\n" + "\n" + "Tämä postaus on generoitu skriptillä: https://github.com/djortsu/ff2/actions/workflows/hoito_alkaa.yml"

print("Start automatic posting...")
post_post(hot_topic, post_content, hot_msg, hot_user, hot_pw)
