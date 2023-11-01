#!/usr/bin/env python3.9
#-*- coding: utf-8 -*-
import json

def fix_languages():
    LANG_CHOICES = [
        ('da', 'Danish'),
        ('en', 'English'),
        ('fo', 'Faroese'),
        ('ine-pro', 'Proto-Indo-European'),
        ('gem-pro', 'Proto-Germanic'),
        ('gwm-pro', 'Proto-West-Germanic'),
        ('ang', 'Old English'),
        ('gmq-osw', 'Old Swedish'),
        ('sv', 'Swedish'),
        ('enm', 'Middle English'),
        ('is', 'Icelandic'),
        ('non', 'Old Norse'),
        ('nn', 'Norwegian Nynorsk'),
        ('nb', 'Norwegian Bokmål'),
    ]

    pk = 1
    entities = []
    
    for lang in LANG_CHOICES:
        entities.append({
            "model": "wordtree.language",
            "pk": pk,
            "fields": {
                "short_name": lang[0],
                "name": lang[1]
            }
        })
        pk += 1

    return entities


def find_language_pk(short_name, languages):
    pks = [x['pk'] for x in languages if x['fields']['short_name'] == short_name]
    return pks[0]


def find_parent(line_index, tree):
    if len(tree) <= line_index:
        return -1
    
    target_indent = tree[line_index].find("- ")
    index = line_index
    while index >= 0:
        line = tree[index]
        indent = line.find("- ")
        if indent < target_indent:
            return index
        index -= 1

    return -2


def fix_words(languages):

    one_tree = [x for x in """
- gem-pro: *ainaz
  - gwm-pro: *ain
    - ang: ān
      - enm: oon
        - en: one
        - en: an
        - en: a
  - non: einn
    - is: einn
    - nn: ein
    - da: en
      - nb: en
    - gmq-osw: ēn
      - sv: en
    """.splitlines() if x.strip() != ""]
    entities = []
    pk = 2
    i = 0

    while i < len(one_tree):
        line = one_tree[i]
        parent_pk = find_parent(i, one_tree)
        if parent_pk < 0:
            parent_pk = 1
        else:
            parent_pk = entities[parent_pk]["pk"]

        language, word = line.lstrip('- ').split(": ")
        language_pk = find_language_pk(language, languages)
        entities.append({
            "pk": pk,
            "model": "wordtree.word",
            "fields": {
                "text": word,
                "reconstructed": True if word[0] == "*" else False,
                "parent": parent_pk,
                "language": language_pk
            }
        })
        pk += 1
        i += 1
    entities.append({
        "pk": 1,
        "model": "wordtree.word",
        "fields": {
                "text": "root",
                "reconstructed": True,
                "parent": 1,
                "language": 1
            }
        })

    return entities
    

def main():
    languages = fix_languages()
    words = fix_words(languages)
    print(json.dumps(languages + words, indent=2))


if __name__ == '__main__':
    main()
