from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join
from tqdm import tqdm
import spacy
from config import *


def extract_sections(filename,soup):
    sections = soup.find_all('section')
    res = []
    num_s = 0
    for s in sections:
        num_s += 1
        txt = " ".join([item.getText() for item in s.find_all(recursive=False)])
        res.append({
            'tag': filename + '#S' + str(num_s),
            'data': txt
        })
    return {'count': num_s, 'data': res}

# considero paragrafi contenenti minimo 5 words
def extract_paragraphs(filename,soup, min_count=5):
    paragraphs = soup.find_all("p")
    res = []
    num_p = 0
    for p in paragraphs:
        txt = p.getText().strip()
        if len(txt.split(" ")) >= min_count:
            num_p += 1
            res.append({
                'tag': filename + '#P' + str(num_p),
                'data': txt
            })
    return {'count': num_p, 'data': res}


# considero frasi con almeno 4 parole
def extract_phrase(filename,soup, lang="en",min_count=5):
    res = []
    text = []
    par = soup.find_all("p")
    for p in par:
        txt = p.getText().strip()
        if len(txt.split()) >= min_count:
            text.append(txt)
    text = " ".join(text)
    nlp = spacy.load(lang + '_core_web_sm')
    doc = nlp(text)
    num_f = 0

    for sent in doc.sents:
        sent = sent.text.strip()
        if len(sent.split()) >= min_count:
            num_f += 1
            res.append({
                'tag': filename + '#F' + str(num_f),
                'data': sent
            })
    return {'count': num_f, 'data': res}

# type = Sezione-Paragrafo-Ngramma-Frase "SPNF"
def process_doc(path, file, type=""):
    html_txt = open(path + file, 'r', encoding='utf-8').read()
    # save_on_file(html_txt,'test.html')
    soup = BeautifulSoup(html_txt, 'html.parser')
    # rimozione del titolo e sottotitolo
    _ = [script.extract() for script in soup('p', {'class': 'doc-ti'})]
    res = []
    if 'S' == type:
        res = extract_sections(file,soup)
    elif 'P' == type:
        res = extract_paragraphs(file,soup)
    elif 'F' == type:
        res = extract_phrase(file,soup)
    elif 'N' == type:
        # TODO:
        res = {}
    return {'filename': file, 'data':res['data'], 'count':res['count']}




def main():
    src_path = "/home/anto/Scrivania/Tesi/dataset/EN/"
    file = "21997A0319(01).html"
    import json
    res = process_doc(src_path,file,type="S")
    # res = process_docs(src_path,"F")
    print(json.dumps(res, indent=4, sort_keys=True))

if __name__ == '__main__':
    main()



