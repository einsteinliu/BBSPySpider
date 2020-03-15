from bs4 import BeautifulSoup
import urllib.request
import wget
import os

def get_all_links(url):
    resp = urllib.request.urlopen(url)
    soup = BeautifulSoup(resp, from_encoding=resp.info().get_param('charset'))
    return soup.find_all('a', href=True)

base_url = "https://bbs.sjtu.edu.cn/"

raw_links = get_all_links("https://bbs.sjtu.edu.cn/bbsboa?sec=5")
d5_links = []
for link in raw_links:
    if "bbsdoc" in link["href"] and "board" in link["href"]:
        if not link["href"] in d5_links:
            d5_links.append(link["href"])

for d5_link in d5_links:
    raw_links = get_all_links(base_url+d5_link)
    for link in raw_links:
        if ".tar.gz" in link["href"]:
            if not os.path.exists(link["href"].replace("/","")):
                wget.download(base_url+link["href"])
    pass
