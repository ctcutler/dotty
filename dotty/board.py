class Board:
    """ Intended to be subclassed and never instantiated directly. """

    def load(self):
        """ Load current board state. """
        raise NotImplementedError()
