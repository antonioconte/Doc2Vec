from os import listdir
from os.path import isfile, join

from gensim.models.doc2vec import TaggedDocument
from preprocess.process_doc import process_doc
from preprocess.text_pipeline import TextPipeline as pipe


class Corpus():
    def __init__(self, path,part):
        self.interval = 250
        self.part = part.upper()
        self.path = path
        self.pipeline_text = pipe()
        self.file_list = [f for f in listdir(self.path) if isfile(join(self.path, f))]
        # self.data = self.__load_docs()

    def __load_doc_items(self,current_file_path):
        return process_doc(self.path,current_file_path,self.part)

    def __iter__(self):
        for d in self.file_list:
            items = self.__load_doc_items(d)
            # yield items
            for item in items['data']:
                words = self.pipeline_text.convert(item['data'])
                tag = "[{}] {}".format(item['tag'],item['data'])
                yield TaggedDocument(words=words,tags=[tag])

        # for (index,item) in enumerate(self.data):
        #     if (index+1) % self.interval == 0:
        #         print("item {}/{}".format(index+1,len(self.data)))


if __name__ == '__main__':
    src_path = "/home/anto/Scrivania/Tesi/dataset/EN/"
    c = iter(Corpus(src_path,"S"))
    a = next(c)
    print(a)
    a = next(c)
    print(a)




    # import json
    # print(json.dumps(indent=4, sort_keys=True))
