#!/usr/bin/env python
import os
import pathlib
import re
import sys
import unicodedata
import urllib.request
import zipfile

import requests
from bs4 import BeautifulSoup

url = sys.argv[1]

r = requests.get(url)

x = r.text
soup = BeautifulSoup(x, features='lxml')
meta = soup.select('.column.col-3')
author = meta[0].get_text().strip().removeprefix("Author: ")
lang = meta[1].get_text().strip().removeprefix("Language: ")
platform = meta[3].get_text().strip().removeprefix(
    "Platform").removesuffix("etc.").strip()
difficulty = meta[4].get_text().strip().removeprefix("Difficulty: ")
quality = meta[5].get_text().strip().removeprefix("Quality: ")
arch = meta[5].get_text().strip().removeprefix("Quality: ")
name = soup.select_one('h3').get_text().removeprefix(f"{author}'s ")
desc = soup.select_one('.column.col-12 p span').get_text()
id = url.split('/')[-1]


def clean_path(value):
    value = str(value)
    value = unicodedata.normalize('NFKD', value).encode(
        'ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


folder = pathlib.Path(clean_path(f"{name}_{id}"))
os.makedirs(folder, exist_ok=True)
os.chdir(folder)

contents = [
    f"# crackme: {author}'s {name}",
    "\n>\n".join("> "+s for s in [f"Name: {name}",
                                  f"Author: {author}",
                                  f"Description: {desc}",
                                  f"Difficulty: {difficulty}",
                                  f"Quality: {quality}"]),
]

with open('README.md', 'w') as f:
    f.write("\n\n".join(contents)+"\n")

zip_path = f'{id}.zip'
urllib.request.urlretrieve(
    f"https://crackmes.one/static/crackme/{id}.zip", zip_path)
zipfile.ZipFile(zip_path).extractall(pwd=b'crackmes.one')
