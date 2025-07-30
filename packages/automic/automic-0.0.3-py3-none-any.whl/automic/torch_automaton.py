class TensorAutomaton:
    def __init__(self, n_states: int, accepting: Set[int]):
        self.n_states = n_states
        self._alphabet_size=1024
        self._sym2idx = {None: 0}
        self._idx2sym = [None]
