path_train = "/home/anto/Scrivania/Tesi/Doc2Vec/data_test/"
training = True
to_save = True
PATH_TO_EXISTING_MODEL = "/home/anto/Scrivania/Tesi/Doc2Vec/model/"
PATH_TO_SAVE_MODEL = "/home/anto/Scrivania/Tesi/Doc2Vec/model/"


NumLoadedDoc = 0
DEBUG = False


# Skip-gram: works well with small amount of the training data, represents well even rare words or phrases.
# CBOW: several times faster to train than the skip-gram, slightly better accuracy for the frequent words
# dm=1, ‘distributed memory’ (SKIP-GRAM). Otherwise, distributed bag of words (CBOW).
DM = 1
ALPHA = 0.025
MIN_ALPHA = 0.00025
WINDOW_CONTEXT = 10
EPOCHS = 500
VECTOR_SIZE = 200
MIN_COUNT = 5
Num_of_Res = 5 # numero di risultati