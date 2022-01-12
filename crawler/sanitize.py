#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# Crawler sanitizing scripts

import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{os.path.split(os.getcwd())[-1]}.settings')
print(os.getcwd())
django.setup()

from wordtree.models import Language

if __name__ == "__main__":
    endings = ["[edit]", ": "]

    for x in endings:
        langs = Language.objects.filter(name__endswith=x)
        for lang in langs:
            old = lang.name
            new = lang.name[:-len(x)]
            print(f"{old} -> {new}")
            lang.name = new

        if len(langs) > 0:
            ok = input("Are these changes OK? [y/n]")
            if ok == "y":
                for lang in langs:
                    lang.save()
                print("Saved.")
            else:
                print("Aborted.")
        else:
            print(f"No changes to make at `{x}`.")
