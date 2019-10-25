import numpy as np
class Generator(object):
    def __init__(self, list_of_sequence: list, pad: bool = True, shuffle: bool = True, batch_size=10):
        self.list_of_sequence = np.random.shuffle(
            list_of_sequence) if shuffle else list_of_sequence
        self.pad = pad
        self.batch_size = 10

    def padding(self, sequence, maxlen, padding='pre', value=0.0):
        if len(sequence) >= maxlen:
            return sequence[:maxlen]
        else:
            num_pad = maxlen - len(sequence)
            pad_array = [value] * num_pad
            if padding == 'pre':
                return pad_array + sequence
            elif padding == 'post':
                return sequence + pad_array

    def encode_pick(self, current, sequence):
        encoder = [int(x) for x in sequence[current:]] + [-1] * (current)
        return encoder

    def __len__(self): return len(self.list_of_sequence)

    def process_training(self, sequence, maxlen=21, is_pad=True):
        x, y = [], []

#         hero     = padding( [s['hero_id'] for s in sequence] ,maxlen=maxlen,padding='post',value=0)
#         pick_ban = padding( [int(s['is_pick']) for s in sequence ], maxlen=maxlen, padding='post',value=-1.)
#         team     = padding( [int(s['team']) for s in sequence    ], maxlen=maxlen,padding = 'post',value=-1.)

        hero = padding([s['hero_id'] for s in sequence], maxlen=maxlen,
                       padding='post', value=-1.) if is_pad else [s['hero_id'] for s in sequence]
        pick_ban = padding([s['is_pick'] for s in sequence], maxlen=maxlen,
                           padding='post', value=-1.) if is_pad else [s['is_pick'] for s in sequence]
        team = padding([s['team'] for s in sequence], maxlen=maxlen,
                       padding='post', value=-1.) if is_pad else [s['team'] for s in sequence]

        placeholder = np.array([np.array([hero[i]] + self.encode_picks(i, pick_ban) + self.encode_picks(i, team)) for i in range(maxlen)])
        x = placeholder[:-1]
        y = placeholder[1:, 0]
        return x, y

    def __iter__(self):
        total_batches = len(self) // self.batch_size
        for i in range(total_batches):
            seq = [self.process_training( arr) for arr in self.list_of_sequence[i*self.batch_size: (i+1)*self.batch_size]]
            x, y = zip(*seq)
            yield np.array(x), np.array(y)
