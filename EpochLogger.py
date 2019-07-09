from gensim.models.callbacks import CallbackAny2Vec
from datetime import datetime
class EpochLogger(CallbackAny2Vec):
    '''Callback to log information about training'''
    def __init__(self):
        self.start = datetime.now()
        self.epoch = 0

    #     def on_epoch_begin(self, model):
    # print("Epoch #{} start".format(self.epoch))

    def on_epoch_end(self, model):
        end = datetime.now()
        time = int((end - self.start).total_seconds())
        minute = time/60.0
        print("> Epoch #{} END - TIME: {}s {}m\n".format(self.epoch,time,minute))
        self.epoch += 1
