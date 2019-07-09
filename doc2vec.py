from config import *
from preprocess.ReadCorpus import Corpus
from gensim.models.doc2vec import Doc2Vec
from EpochLogger import EpochLogger
from preprocess.text_pipeline import TextPipeline as pipe
from datetime import datetime
import multiprocessing

class Doc2Vec_model(object):
    def __init__(self,type="",path=""):
        self.part = type.upper()
        self.train_corpus = path
        self.epoch_logger = EpochLogger()
        self.pipe = pipe()
        self.PATH_SAVE = PATH_TO_SAVE_MODEL + self.part + ".d2v"
        self.model = None

    def train(self):
        cores = multiprocessing.cpu_count()
        print(self.part + "- Analizzando...")

        print('\nReading training corpus from %s' % self.train_corpus)
        corpus_data = Corpus(self.train_corpus,self.part)

        self.model = Doc2Vec(
            vector_size=VECTOR_SIZE,
            alpha=ALPHA, min_alpha=MIN_ALPHA, min_count=MIN_COUNT,
            window=WINDOW_CONTEXT, dm=DM,
            callbacks=[self.epoch_logger],workers=cores
        )

        print('\n- Building Vocabulary... In base ad ogni item estratto genero il vocabolario')
        self.model.build_vocab(corpus_data)

        print("\n-[Cores: {}] Training...".format(cores))
        self.model.train(corpus_data, total_examples=self.model.corpus_count, epochs=EPOCHS)

        if to_save:
            self.model.save(self.PATH_SAVE)
        print('\nTotal docs learned %s' % (len(self.model.docvecs)))
        return self.model

    def get(self):
        return self.model

    def load(self):
        PATH = PATH_TO_EXISTING_MODEL + self.part + ".d2v"
        print('loading an exiting model {}'.format(PATH))
        self.model = Doc2Vec.load(PATH)
        return PATH

    def __check(self):
        if self.model == None:
            print("Before LOAD MODEL!!!")
            exit(1)

    def gen_vec(self,words):
        self.__check()
        vector = self.model.infer_vector(words)
        return vector

    def most_similar(self,v,N=0):
        if N == 0:
            return self.model.docvecs.most_similar([v])
        else:
            return self.model.docvecs.most_similar([v],topn=N)

    def predict(self,txt):
        self.__check()
        start = datetime.now()
        words = self.pipe.convert(txt) # text normalized
        vector = self.gen_vec(words)   # embedding
        sims = self.model.docvecs.most_similar([vector], topn=Num_of_Res)
        end = datetime.now()
        time = str(round((end - start).total_seconds(), 3) * 1000) + "ms"
        print("Time :", time)
        return (time,sims)

def train(src_path,type):
    model = Doc2Vec_model(type=type, path=src_path)
    model.train()

def test(txt,type="S"):
    model = Doc2Vec_model(type=type)
    model.load()
    import json
    res = model.predict(txt)
    print(json.dumps({ 'query':txt, 'res':res}, indent=4, sort_keys=True))


if __name__ == '__main__':

    # src_path = path_train
    # print('PATH TRAIN: ',path_train)
    # train(src_path, type="S")
    #
    txt = """
    Article 18 Competent authority Member States shall make the appropriate administrative arrangements, 
    including the designation of the appropriate competent authority or authorities, for the implementation 
    of the rules of this Directive. Where more than one competent authority is designated, the work of these 
    authorities undertaken pursuant to this Directive must be coordinated.",      
    """

    # test(txt,type="S")

    model = Doc2Vec_model(type="S")
    path = model.load()
    txt_edit = model.pipe.convert(txt)
    print(txt_edit)
    vector = model.gen_vec(txt_edit)
    knn = model.most_similar(vector)
    import json
    print(json.dumps({'query':txt, 'res': knn}, indent=4, sort_keys=True))
    # v1 = model.infer_vector(txt_edit)

