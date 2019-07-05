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

    src_path = path_train
    print('PATH TRAIN: ',path_train)
    train(src_path, type="S")

    # txt = """THE COMMISSION OF THE EUROPEAN COMMUNITIES,
    # Having regard to the Treaty establishing the European Community,
    # Having regard to Council Regulation (EC) No 510/2006 of 20 March 2006 on the protection of geographical indications and designations of origin for agricultural products and foodstuffs, and in particular the first subparagraph of Article 7(4) thereof,
    # Whereas:
    # (1) Pursuant to the first subparagraph of Article 6(2) and in accordance with Article 17(2) of Regulation (EC) No 510/2006, France’s application to register the name ‘Moutarde de Bourgogne’ was published in the Official Journal of the European Union .
    # (2) As no objections within the meaning of Article 7 of Regulation (EC) No 510/2006 were received by the Commission, this name should be entered in the register,
    # HAS ADOPTED THIS REGULATION:"""
    #
    # test(txt,type="S")
