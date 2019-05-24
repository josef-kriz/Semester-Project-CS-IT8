class Config:
    def __init__(self):
        # True if running multiple architectures, for finding best configuration
        # False if running HIDDEN_LAYERS from Config.
        self.MULTIPLE_ARCHITECTURES = True
        # if MULTIPLE_ARCHITECTURES is True, all of these will run instead of other Configs.

        self.TEST_LAYERS_MIN = 5  # NOTE, if changing this, u need to change what is written to file.
        self.TEST_LAYERS_MAX = 5  # NOTE, if changing this, u need to change what is written to file.
        self.TEST_NOTES = [128, 256]
        self.TEST_REGULARIZERS = ['none','l1']
        self.TEST_ACTIVATION_FUNCTIONS = ['relu', 'tanh']
        self.TEST_CLASS_WEIGHTS = [1., 40.]

        # if not testing multiple configurations, these will be used.
        self.HIDDEN_LAYERS = [128, 32]  # 0.656
        self.REGULARIZER = None
        self.ACTIVATION_FUNCTION = 'relu'
        self.CLASS_WEIGHT = {0: 1., 1: 30.}

        # This is not the amount of epochs, but the cap (if using early stopping)
        self.EPOCHS = 200
        self.BATCH_SIZE = 20
        self.EARLY_STOPPING = True
        self.EARLY_STOPPING_PATIENCE = 2

        self.BIAS = True
        self.LOSS = 'binary_crossentropy'
        self.OPTIMIZER = 'adam'
        self.SHUFFLE = False

        self.TRAINING_CUT = 0.7
        # set to 0 for normal ratio from pickle file.
        self.NEGATIVE_SAMPLES_RATIO = 0

        self.FILE = 'output/full-24hours-aggr-mean-shuffled.pickle'
