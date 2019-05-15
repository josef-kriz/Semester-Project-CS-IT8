from keras import losses
from keras.optimizers import *


class Config:
    def __init__(self):
        #True if running multiple architectures, for finding best HIDDEN_LAYERS
        #False if running HIDDEN_LAYERS from Config.
        self.MULTIPLE_ARCHITECTURES = True
        self.TEST_LAYERS = 5
        self.TEST_NOTES = [32, 64, 256]

        # This is not the amount of epochs, but the cap
        self.EPOCHS = 100
        self.BATCH_SIZE = 20
        self.EARLY_STOPPING = True
        self.EARLY_STOPPING_PATIENCE = 2

        self.HIDDEN_LAYERS = [128, 64, 32]

        self.BIAS = True
        self.LOSS = 'binary_crossentropy'
        self.OPTIMIZER = 'adam'
        self.ACTIVATION_FUNCTION = 'tanh'
        self.SHUFFLE = False

        self.TRAINING_CUT = 0.8
        #set to 0 for normal ratio from pickle file
        self.NEGATIVE_SAMPLES_RATIO = 0
        self.CLASS_WEIGHT = {0: 1., 1: 30.}

        self.FILE = 'training.pickle'
