import json
from os import listdir
from os.path import isfile, join
from config import *
import os

from bs4 import BeautifulSoup

def remove_tag(text):
    soup = BeautifulSoup(text,'html.parser').find_all(recursive=False)
    print(soup)
    text = [item.getText() for item in soup]
    return " ".join(text)

def save_on_file(text, path):
    Html_file = open(path, "w")
    Html_file.write(text)
    Html_file.close()

def make_doclist():
    files_name = [f for f in listdir(path_train) if isfile(join(path_train, f))]
    print(len(files_name))
    res = {
        'path': path_train,
        'docs': files_name
    }
    json_file = json.dumps(res, indent=4, sort_keys=True)
    save_on_file(json_file, './doclist.json')



if __name__ == '__main__':
    # make_doclist()
    print("HELLO IN UTILS")
