from crawler import Word, Article, encode_url, tag_to_word, App
from bs4 import BeautifulSoup as Soup

print("===")
print("## Test Article")
url = 'https://en.wiktionary.org/wiki/Reconstruction:Proto-West_Germanic/bikkjan'
art = Article(url)

for root in art.find_roots():
	print(root)
	print(repr(
		[x for x in art.sections[root['in_section']]['content'] if x.name == "ul"]
	)[:100])


print("\n===")
print("## Test tag to word")
htmls = ["""<li>Nepali: <span class="Deva" lang="ne"><a href="/wiki/%E0%A4%B8%E0%A5%81%E0%A4%AA%E0%A4%BE%E0%A4%B0%E0%A5%80#Nepali" title="सुपारी">सुपारी</a></span> <span class="mention-gloss-paren annotation-paren">(</span><span lang="ne-Latn" class="tr Latn">supārī</span><span class="mention-gloss-paren annotation-paren">)</span><link rel="mw-deduplicated-inline-style" href="mw-data:TemplateStyles:r54857417"></li>""",
'<p><strong class="Brah headword" lang="inc-ash">*𑀲𑀼𑀧𑁆𑀧𑀸𑀭</strong> (<span lang="inc-ash-Latn" class="headword-tr tr Latn" dir="ltr">*suppāra</span>)<sup id="cite_ref-1" class="reference"><a href="#cite_note-1">[1]</a></sup>\n</p>',
'<li><span class="desc-arr" title="borrowed">→</span> English: <span class="Latn" lang="en"><a href="/wiki/supari#English" title="supari">supari</a></span><link rel="mw-deduplicated-inline-style" href="mw-data:TemplateStyles:r54857417"></li>',
'<p><strong class="Brah headword" lang="inc-ash">*𑀅𑀝𑁆𑀝𑀓𑁆𑀓𑀮𑀸</strong> (<span lang="inc-ash-Latn" class="headword-tr tr Latn" dir="ltr">*aṭṭakkalā</span>)&nbsp;<span class="gender"><abbr title="feminine gender">f</abbr></span></p>'
]
soups = [Soup(x, "lxml") for x in htmls]
tags = [soups[0].li, soups[1].p, soups[2].li, soups[3].p]
words = [
    Word("सुपारी", "ne", "Nepali", "supārī"),
    Word("*𑀲𑀼𑀧𑁆𑀧𑀸𑀭", "inc-ash", romanized="*suppāra"),
    Word("supari", "en", "English"),
    Word("*𑀅𑀝𑁆𑀝𑀓𑁆𑀓𑀮𑀸", "inc-ash", romanized="*aṭṭakkalā"),
]
for i in range(len(tags)):
	tag = tags[i]
	expected = words[i]
	actual = tag_to_word(tag)
	print(f"Checking {expected}:")
	print(actual.word, end='')
	if actual.word == expected.word:
		print(" OK")
	else:
		print(f" failed, expected {expected.word}")
	print(actual.language, end='')
	if actual.language == expected.language:
		print(" OK")
	else:
		print(f" failed, expected {expected.language}")
	print(actual.romanized, end='')
	if actual.romanized == expected.romanized:
		print(" OK")
	else:
		print(f" failed, expected {expected.romanized}")
	print(actual)


print("\n===")
print("## Test Romanization")
url = encode_url('https://en.wiktionary.org/wiki/Reconstruction:Ashokan_Prakrit/𑀅𑀝𑁆𑀝𑀓𑁆𑀓𑀮𑀸')
art = Article(url)
app = App("wordtree/crawler/test_config.json")

for root in art.find_roots():
	lists = [app.ul_to_words(x) for x in art.sections[root['in_section']]['content'] if x.name == "ul"]
	for li in lists:
		for word in li:
			root['word'].add_child(word)

print(root['word'].tree())


print("\n===")
print("## Test tree building")
url = encode_url('https://en.wiktionary.org/wiki/Reconstruction:Proto-Germanic/þaką')
art = Article(url)
app = App("wordtree/crawler/test_config.json")

for root in art.find_roots():
	section = art.sections[root['in_section']]['content']
	lower = [i for i in range(len(section)) if section[i].text == "Descendants[edit]"][0]
	section = section[lower+1:]

	lists = [app.ul_to_words(x) for x in section if x.name == "ul"]
	for li in lists:
		for word in li:
			root['word'].add_child(word)

print(root['word'].tree())
