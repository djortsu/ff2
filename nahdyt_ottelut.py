# usage:
# python3 nahdyt_ottelut.py -i http://futisforum2.org/index.php?topic=<topic_id> -p <page_count>
# e.g. python3 nahdyt_ottelut.py -i http://futisforum2.org/index.php?topic=263126 -p 4
# dependencies:
# install Python 3.10.4 or newer
# python3 -m pip install bs4==0.0.1
# python3 -m pip install requests==2.27.1

from bs4 import BeautifulSoup
from collections import OrderedDict
import argparse
import re
import requests
import sys

def get_page_count(input_page):
    response = requests.get(input_page)
    soup = BeautifulSoup(response.content.decode('iso-8859-1'), 'html.parser')
    for y1 in soup.find_all('div', class_='middletext wordspacing'):
        if "Sivuja: [" in y1.get_text():
            if y1.get_text()[-2] == "]":
                return 1
            else:
                return int(y1.get_text().split(" ")[-2])

def parse_page(input_page, i):
    page_index = i*25
    print("parsing page " + input_page + "." + str(page_index))
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
                if x1.string not in nicks:
                    nicks.append(x1.string)
    for y1 in soup.find_all('div'):
        if y1.get('class') == ['saihe']:
            id = y1.get('id').split("_")[1]
            links.append(input_page.split("=")[0] + "=" + topic + ".msg" + id + "#msg" + id)
    
    nick_link_dict = {nicks[i]: links[i] for i in range(len(nicks))}

    return nick_link_dict

def make_post(dict):
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
        print(item)

parser = argparse.ArgumentParser()

parser.add_argument('-i', '--input', required=True)
#parser.add_argument('-p', '--page_count', type=int, required=True)

args = parser.parse_args()

page_count = get_page_count(args.input)
print("page count = " + str(page_count))


full_nick_link_dict = {}

for i in range(page_count):
    nick_link_dict = parse_page(args.input, i)
    full_nick_link_dict.update(nick_link_dict)

sorted_nick_link_dict = OrderedDict(sorted(full_nick_link_dict.items(), key=lambda x: x[0].lower()))

make_post(sorted_nick_link_dict)
print("\n" + "Foorumisteja: " + str(len(sorted_nick_link_dict)))