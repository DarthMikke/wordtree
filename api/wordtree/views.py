import os
import subprocess

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django import forms
from .models import Word


# Create your views here.
def image(request, word_pks):
    (_, file_format) = os.path.splitext(request.get_full_path())
    file_format = file_format[1:]
    word_pks = [int(x) for x in word_pks.split(",")]

    lines = ["digraph {"]
    words = []

    for word_pk in word_pks:
        word = Word.objects.get(id=word_pk)
        print(word)
        children = Word.objects.filter(parent=word)
        for child in children:
            words.append(child)

        while word.id != 1:
            if len([x for x in words if x.id == word.id]) == 0:
                words.append(word)
            word = word.parent
            print(word)

    lines += [f"""W{x.id} [label=<{x.text}<BR/>({x.language.name})>]"""
              for x in words]
    lines += [f"W{x.parent.id} -> W{x.id}" for x in words if x.parent.id != 1]
    lines += ["}"]

    print("\n".join(lines))

    process = subprocess.run(
        ["dot", f"-T{file_format}", "-Gsize=900,1500!", "-Gdpi=100"],
        input="\n".join(lines).encode("utf-8"),
        capture_output=True)
    if process.stderr != b'':
        print(process.stderr.decode())

    output = process.stdout.decode() if file_format == "svg" \
        else process.stdout

    return HttpResponse(output, content_type=f"image/{file_format}")


class WordForm(forms.Form):
    words = forms \
            .ModelMultipleChoiceField(
                queryset=Word.objects.exclude(id=1).order_by('text')
            )


def index(request):
    return render(request, 'wordtree/index.html', {'form': WordForm})


def search(request):
    query = request.GET['query']
    queryset = Word.objects \
        .filter(text__contains=query) \
        .exclude(approved=False).exclude(id=1)
    suggestions = [
        {
            'id': x.id,
            'word': x.text,
            'latin': '',
            'language': x.language.short_name,
            'language_full': x.language.name
        } for x in queryset
    ]
    return JsonResponse({'suggestions': suggestions})


def tree(request):
    """
    This view is not used in the React app.
    """
    word_pks = request.META['QUERY_STRING']
    word_pks = [x.rstrip("&") for x in word_pks.split("words=")]
    word_pks[-1] = word_pks[-1].split("&")[0]
    word_pks = [x for x in word_pks if len(x) > 0]
    print(word_pks)
    word_pks = [int(x) for x in word_pks if len(x.split("=")) == 1]
    words = [Word.objects.get(id=x) for x in word_pks]
    words = [(x.text, x.language.name) for x in words]
    word_pks = ",".join([str(x) for x in word_pks])

    return render(request, 'wordtree/tree.html', {'form': WordForm, 'words': words, 'pks': word_pks})
