import random
import subprocess
import requests

BASE_URL = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles={}"


words = [x.strip() for x in open("bad_words.txt").readlines()]
fnames = [x.strip() for x in open("first_names.txt").readlines()]
lnames = [x.strip() for x in open("last_names.txt").readlines()]

NUM = 300

template = open("formal_letter_3.tex").read()
fname = "document_{:03d}.tex"


for i in range(NUM):
    name = random.choice(fnames) + " " + random.choice(lnames)
    info = None

    while not info:
        word = random.choice(words)
        r = requests.get(BASE_URL.format(word))
        e = None
        try:
            e = list(r.json()["query"]["pages"].values())[0]['extract']
        except KeyError:
            pass
        if e and "may refer" not in e:
            info = e
    tmp_f = fname.format(i + 1)

    tmp_text = template.replace("$NAME$", name)
    tmp_text = tmp_text.replace("$INFO$", info)
    tmp_text = tmp_text.replace("$TITLE$", word)
    with open(tmp_f, "w") as f:
        f.write(tmp_text)

    subprocess.call("pdflatex -halt-on-error {}".format(tmp_f), shell=True)