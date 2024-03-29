#!/usr/bin/env python3.9
import os
import sys
import django
import json
import argparse

from urllib.parse import urlsplit, urlunsplit, urlparse, quote
from urllib.request import urlopen
from bs4 import BeautifulSoup as Soup

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{os.path.split(os.getcwd())[-1]}.settings')
print(os.getcwd())
django.setup()

import wordtree.models as models


class Logger:
    def __init__(self, logfile):
        self.logfile = logfile

    def log(self, x, end='\n'):
        with open(self.logfile, "a") as fh:
            fh.write(f"{x}{end}")


class Word:
    def __init__(self, word, language, language_full="Unknown", romanized=None):
        self.word = word
        self.romanized = romanized
        self.language = language
        self.language_full = language_full
        self.children = []

    def add_child(self, child):
        print(f"{self} -> {child}")
        if type(child) != type(self):
            raise TypeError(f"{child} is not a word.")
        if child == self:
            raise ValueError("Can't self-reference.")
        if child.word is None:
            for grandchild in child.children:
                self.add_child(grandchild)
            return

        self.children.append(child)

    def tree(self):
        if len(self.children) == 0:
            return str(self)
        trees = [str(x.tree()) for x in self.children]
        trees = "\n".join(trees)
        trees = ["  " + str(x) for x in trees.splitlines()]
        return str(self) + "\n" + "\n".join(trees)

    def __repr__(self):
        return f"<{str(self)})>"

    def __str__(self):
        word = f"{self.word}"
        if not (self.romanized == self.word or self.romanized is None):
            word = f"{self.word}/{self.romanized}"
        return f"{word} ({self.language}/{self.language_full})"


class Article:
    def __init__(self, url):
        self.url = url

        html = None
        with urlopen(url) as fh:
            try:
                html = fh.read()
            except Exception as e:
                raise e

        soup = Soup(html, "lxml")
        self.title = soup.head.title.text
        self.sections = Article.split_to_sections(soup)

    def split_to_sections(soup):
        h2s = soup.find_all("h2")
        sections = []

        for x in h2s:
            header = x
            content = []
            cur = header.next_sibling
            while cur is not None:
                content.append(cur)
                cur = cur.next_sibling
            sections.append({"header": header, "content": content})
        return sections

    def find_roots(self):
        roots = []
        i = 0

        while i < len(self.sections):
            section = self.sections[i]
            j = 0
            found_h3 = False
            seek = True
            while seek and j < len(section['content']):
                cur = section['content'][j]
                if cur.name == "h3":
                    found_h3 = True
                elif found_h3:
                    if cur.name == "p":
                        if not cur.next is None:
                            if cur.next.name is not None and cur.next.has_attr("lang"):
                                seek = False
                                break
                            else:
                                found_h3 = False
                    elif cur.name is not None and cur.name != "p":
                        found_h3 = False
                j += 1
            if not seek:
                word = tag_to_word(cur)
                word.language_full = section['header'].text
                roots.append({'word': word, "in_section": i})
            i += 1

        return roots


def tag_to_word(tag):
    """
    Wiktionary words are expressed as:
    [<arrow>] [<Full language name>: ] <word> [(<romanized word>)]
    """
    word = None
    language = None
    language_full = None
    romanized = None
    cur = tag.next
    while True:
        if cur is None:
            # print("")
            break
        # print(cur, repr(cur.name), end='')
        if cur.name is None:
            if language_full is None:
                # print(", saved as `language_full`")
                language_full = cur.string
        else:
            if cur.has_attr("lang"):
                # print("lang:", cur['lang'])
                if cur.has_attr("class"):
                    # print("class:", cur['class'])
                    if "tr" in cur['class']:
                        # print(", saved as `romanized`")
                        romanized = cur.text
                    else:
                        # print(", saved as `word`")
                        language = cur['lang']
                        # print(f"{language} saved as `language`")
                        word = cur.text
                else:
                    word = cur.text
            else:
                if cur.has_attr("class"):
                    # print("class:", cur['class'])
                    if "desc-arr" in cur['class']:
                        # print(", recognized as `arrow`")
                        pass
        cur = cur.next_sibling
    return Word(word, language, language_full, romanized)


class App:
    logmessage = "Encountered error. Check log file for details."

    def __init__(self, state_uri, url=None, save=False):
        self.state_uri = state_uri
        if state_uri is not None:
            if not os.path.isfile(state_uri):
                self.state = {"file_id": 0, "line_no": 0, "file_base": "wordtree/crawler/urls-{}.txt",
                              "logfile": "./crawler.log"}
                self.write_state()

        if state_uri is None:
            self.save = save
            self.state = {"file_id": 0, "line_no": 0, "file_base": "wordtree/crawler/urls-{}.txt",
                          "logfile": "./crawler.log"}
        else:
            self.save = True

        if state_uri is not None:
            with open(state_uri) as fh:
                state_text = fh.read()
                self.state = json.loads(state_text)

                self.load_urls()
        else:
            self.urls = [url]

        if 'logfile' not in self.state.keys():
            self.state['logfile'] = './crawler.log'

        self.logger = Logger(self.state['logfile'])

        self.write_state()

    def load_urls(self):
        if self.state_uri is None:
            return
        with open(self.state['file_base'].format(self.state['file_id'])) as fh:
            self.urls = [f"https://en.wiktionary.org{url}" for url in fh.read().splitlines()]

    def write_state(self):
        if self.state_uri is None:
            return
        with open(self.state_uri, "w") as fh:
            fh.write(json.dumps(self.state))
            fh.write("\n")

    def next_url(self):
        if self.state_uri is None:
            return self.urls[0]
        if self.state['line_no'] >= len(self.urls):
            self.state['file_id'] += 1
            self.state['line_no'] = 0
            self.load_urls()

        url = self.urls[self.state['line_no']]
        # url = encode_url(url)
        return url

    def load_next_url(self):
        self.state['line_no'] += 1
        self.write_state()
        url = self.next_url()
        article = Article(url)
        self.logger.log(f"OK: {url}")
        return article

    def ul_to_words(self, ul):
        # print(f"Analyzing ul starting with {ul.text[:40]}")
        words = []

        ul = list(ul.find_all("li", recursive=False))
        for li in ul:
            word = tag_to_word(li)

            child_ul = li.find_all("ul", recursive=False)
            if len(child_ul) > 0:
                child_ul = child_ul[0]
                # ul_to_words(child_ul, word)
                for child_word in self.ul_to_words(child_ul):
                    try:
                        word.add_child(child_word)
                    except Exception as e:
                        print(App.logmessage)
                        self.logger.log(f"Fail 1: {e}")

            words.append(word)

        return words

    def word_to_django_word(self, word: Word, source: str = ""):
        language = None
        try:
            language = models.Language.objects.get(short_name=word.language)
        except models.Language.DoesNotExist:
            try:
                language = models.Language.objects.create(short_name=word.language, name=word.language_full)
            except Exception as e:
                self.logger.log(f"Fail 6. Could not add {word}: {e}")

        django_word = None
        self.logger.log(f"Processing {word}...")
        try:
            django_word = models.Word.objects.get(text=word.word, language=language)
            print(f"{word} exists already")
            self.logger.log(f"{word} not added, exists already.")
        except models.Word.DoesNotExist:
            self.logger.log(f"Does not exist yet, attempting to add... ", end='')
            try:
                django_word = models.Word.objects.create(
                    text=word.word,
                    romanized="" if word.romanized is None else word.romanized,
                    language=language,
                    parent=models.Word.objects.get(id=1),
                    source=source)
            except Exception as e:
                self.logger.log(f"Failed.\nFail 5. {e}")
            else:
                self.logger.log(f"OK.")

        for child in word.children:
            django_child = self.word_to_django_word(child, source)
            django_child.parent = django_word
            django_child.save()

        return django_word

    def run(self, n=None):
        if n is None:
            if self.state_uri is None:
                n = 1
            else:
                n = 10

        for i in range(n):
            try:
                article = self.load_next_url()
            except Exception as e:
                print(App.logmessage)
                self.logger.log(f"Fail 2: {e}")
                continue

            print(article.title)
            try:
                roots = article.find_roots()
            except Exception as e:
                print(App.logmessage)
                self.logger.log(f"Fail 3: {e}")
                continue

            # roots = find_roots(soup) # Word("þaką", "gem-pro")
            if len(roots) == 0:
                self.logger.log("Did not find any roots.")
                continue
            for root in roots:
                print(f"Found root {root['word']}")

                print("Looking for section 'Descendants'.")
                section = article.sections[root['in_section']]['content']
                lower = [i for i in range(len(section)) if section[i].text == "Descendants[edit]"]
                uls = []
                if len(lower) > 0:
                    section = section[lower[0] + 1:]
                    uls = [x for x in section if x.name == "ul"]
                if len(lower) < 1 or len(uls) < 1:
                    print("No descendants found.")
                    continue
                uls = [self.ul_to_words(x) for x in uls]

                for ul in uls:
                    for word in ul:
                        if word.word is None or word.language is None:
                            continue
                        root['word'].add_child(word)
                self.logger.log(f"Adding root word {root['word']}...")
                print(root['word'].tree())
                if self.save:
                    try:
                        self.word_to_django_word(root['word'], source=article.url)
                    except Exception as e:
                        print(App.logmessage)
                        self.logger.log(f"\nFail 4 (failed adding root word {root['word']}): {e}")
                        continue
                self.logger.log(f"Root word {root['word']} processed successfully.")

        return


# https://stackoverflow.com/questions/22734464/unicodeencodeerror-ascii-codec-cant-encode-character-xe9-when-using-ur
def encode_url(raw_url):
    url = urlparse(raw_url)._asdict()
    url["path"] = quote(url["path"])
    return urlunsplit((url["scheme"], url["netloc"], url["path"], url["params"], url["query"]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="I read Wiktionary.")
    parser.add_argument("-s", "--save", help="Save the result.", action='store_true', dest='save')
    parser.add_argument("-u", help="URL to parse.", required=False, dest='url')
    args = parser.parse_args()

    # url = "https://en.wiktionary.org/wiki/Reconstruction:Proto-Germanic/þaką"
    if args.url is not None:
        if args.save:
            print("Warning! The result of this Wiktionary lookup will be saved in the database.")
        url = args.url
        if len([y for y in [ord(x) for x in url] if y >= 128]) > 0:
            url = encode_url(url)

        CONFIG = None
        app = App(CONFIG, url, args.save)
        app.run()

        if not args.save:
            print("This search will not be saved. Run with the '-s' flag to save the result.")
        exit()

    CONFIG = "wordtree/crawler/crawler_config.json"
    app = App(CONFIG)
    app.run()
    exit()
