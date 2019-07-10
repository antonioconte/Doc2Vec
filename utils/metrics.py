import textdistance
from preprocess import text_pipeline
import datetime

def Levenshtein(txt1,txt2):
    # print("1:",txt1)
    # print("2:",txt2)
    lev = textdistance.Levenshtein()
    value = lev.normalized_similarity(txt1,txt2)
    return '%.2f' % lev.normalized_similarity(txt1,txt2)
    #value = lev.distance(txt1,txt2) 
    #return round_toN(value,N="0")

def Jaccard(txt1,txt2):
    jac = textdistance.Jaccard()
    value = jac.similarity(txt1,txt2)
    return round_toN(value)



def round_toN(number,N="2"):
    return ('%.'+N+'f') % number

def normalized_text(text,p):
    # rimuova il 'tag' da text [ ..... ] testo considerato
    txt_edited = text.split("]")[1].strip()
    return ' '.join(p.convert(txt_edited))


def distance_metrics(ref,item,pipe):
    text_normalized = normalized_text(item[0], pipe)
    res = {
        'text': item[0]
        , 'text_normalized': text_normalized
        , 'cosine': item[1]
        , 'lev': Levenshtein(ref, text_normalized)
        #, 'lev': 0

        , 'jac': Jaccard(ref,text_normalized)
    }
    return res

def compute(ref,res):
    #ref: stringa di riferimento
    p = text_pipeline.TextPipeline()
    ref = ' '.join(p.convert(ref))
    start = datetime.datetime.now()
    newRes = [
        distance_metrics(ref,item,p)
        for item in res
    ]
    end = datetime.datetime.now()
    time = str((end - start).total_seconds() )+ "s"
    print("Time Lev:", time)

    return (ref,newRes)


