import re
from os import listdir
from os.path import isfile, join
from bs4 import BeautifulSoup
from tqdm import tqdm


def define_style(item):
    tag_class = item.get('class')
    if tag_class != None:
        tag_class = tag_class[0]
        if tag_class== "ti-art":
            item['style'] = "font-style: italic;  text-align: center;"
        elif tag_class == "doc-ti":
            item['style'] = "font-weight: 600; font-style: italic;  text-align: center;"

    return item

def format_html(text):
    childs = text.find_all(recursive=False)
    parsed = []
    for c in childs:
        c = define_style(c)
        valid = " ".join(str(c).split())
        parsed.append(valid)
    return BeautifulSoup(" ".join(parsed), 'html.parser')

def cleanMe(soup):
    for script in soup(["div","hr"]): # remove all javascript and stylesheet code
        script.extract()
    for script in soup('p',{'class':'note'}):
        script.extract()

    return soup

def save_on_file(text,path):
    Html_file = open(path, "w")
    Html_file.write(text)
    Html_file.close()

def create_section(soup):
    sections = []
    num_s = 0
    head_text = ""

    for script in soup('p',{'class':'doc-ti'}):
        script.extract()
        head_text += str(script)

    head_table = soup.find_all('table')[0]
    head_table.extract()

    #remove all anchor
    _ = [ item.extract() for item in soup.find_all("a")]

    section_text = ""

    for c in soup.find_all(recursive=False):
        tag_class = c.get('class')
        if tag_class != None and 'ti-art' in tag_class:
            num_s +=1
            sections.append("<section>{}</section>".format(section_text))
            section_text = ""
        section_text += str(c)
    sections.append("<section>{}</section>".format(section_text))
    return head_text + (" ".join(sections))

def main():
    src_path = "./dataset/"
    dst_path = "./scraped/"
    # dst_path = "/home/anto/Scrivania/Tesi/dataset/EN/"

    files_name = [f for f in listdir(src_path) if isfile(join(src_path, f))]

    # for d in ['31997D0622.html']:
    for d in tqdm(files_name):
        # print(d)
        text = BeautifulSoup(open(src_path + d, 'r', encoding='utf-8').read(), 'html.parser')
        text = cleanMe(text)
        text = format_html(text)
        text = create_section(text)
        # print(text)
        save_on_file(text, dst_path + d)


if __name__ == '__main__':
    main()
