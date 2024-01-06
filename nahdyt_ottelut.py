from bs4 import BeautifulSoup
from collections import OrderedDict
import argparse
import requests

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
    #print("parsing page " + input_page + "." + str(page_index))
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

args = parser.parse_args()

page_count = get_page_count(args.input)
#print("page count = " + str(page_count))


full_nick_link_dict = {}

for i in range(page_count):
    nick_link_dict = parse_page(args.input, i)
    if i == 0:
        del nick_link_dict[next(iter(nick_link_dict))]
    full_nick_link_dict.update(nick_link_dict)

sorted_nick_link_dict = OrderedDict(sorted(full_nick_link_dict.items(), key=lambda x: x[0].lower()))

make_post(sorted_nick_link_dict)
print("\n" + "Foorumisteja: " + str(len(sorted_nick_link_dict)))
print("\n" + "Vanhat:")
print("[url=http://futisforum2.org/index.php?topic=263126]2023[/url]")
print("[url=http://futisforum2.org/index.php?topic=254623]2022[/url]")
print("[url=http://futisforum2.org/index.php?topic=242684]2021[/url]")
print("[url=http://futisforum2.org/index.php?topic=234715]2020[/url]")
print("[url=http://futisforum2.org/index.php?topic=224630]2019[/url]")
print("[url=http://futisforum2.org/index.php?topic=214095]2018[/url]")
print("[url=http://futisforum2.org/index.php?topic=203315]2017[/url]")
print("[url=http://futisforum2.org/index.php?topic=190345]2016[/url]")
print("[url=http://futisforum2.org/index.php?topic=178127]2015[/url]")
print("[url=http://futisforum2.org/index.php?topic=163350]2014[/url]")
print("[url=http://futisforum2.org/index.php?topic=150525]2013[/url]")
print("[url=http://futisforum2.org/index.php?topic=133276]2012[/url]")
print("[url=http://futisforum2.org/index.php?topic=114936]2011[/url]")
print("[url=http://futisforum2.org/index.php?topic=92118]2010[/url]")
print("[url=http://futisforum2.org/index.php?topic=63884]2009[/url]")
print("[url=http://futisforum2.org/index.php?topic=42920]2008[/url]")
print("[url=http://futisforum2.org/index.php?topic=10358]2007[/url]")
print("[url=http://futisforum2.org/index.php?topic=1109]2006[/url]")
print("\nTämä postaus on generoitu skriptillä: https://github.com/djortsu/ff2/actions/workflows/hoito_alkaa.yml")
