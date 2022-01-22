import sys
from bs4 import BeautifulSoup as Soup
from urllib.request import urlopen

# Original URL: "https://en.wiktionary.org/w/index.php?title=Special:AllPages&from=Old+Dutch%2Fbar&namespace=118"
try:
    url = sys.argv[-1] if len(sys.argv) < 2 else input("url: ")
except KeyboardInterrupt:
    exit()

with urlopen(url) as fh:
    html = fh.read()

soup = Soup(html, "lxml")
hrefs = [
    y['href'] for y in [
        x for x in soup.find_all('a') if x.has_attr('href')
    ]
]
for href in hrefs:
    print(href)
