from keras import losses
from keras.optimizers import *


class Config:
    def __init__(self):
        # This is not the amount of epochs, but the cap
        self.EPOCHS = 4
        self.BATCH_SIZE = 32

        self.HIDDEN_LAYERS = [10]

        self.BIAS = True
        self.LOSS = 'binary_crossentropy'
        self.OPTIMIZER = 'adam'
        self.ACTIVATION_FUNCTION = 'tanh'
        self.SHUFFLE = True

        self.TRAINING_CUT = 0.7
        self.NEGATIVE_SAMPLES_RATIO = 800

        self.FILE = 'training.pickle'
