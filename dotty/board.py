class Board:
    ''' Intended to be subclassed and never instantiated directly. '''

    def __init__(self, token):
        raise NotImplementedError()

    def load(self):
        ''' Load current board state. '''
        raise NotImplementedError()
