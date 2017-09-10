import numpy as np
import random
import time

def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        return result + (te - ts,)

    return timed

@timeit
def ANNEAL(initial_state, E, kmax=10000):
    def P(e, enew, ti):
        if enew - e < 0:
            return 1
        else:
            return np.exp(-(enew - e) / ti)
    def T(x):
        return 1 / (1 + x)
    s = initial_state
    for k in range(kmax):
        t = T(k / kmax)
        snew = random.choice(s.successors())
        e = getattr(s, E)()
        enew = getattr(snew, E)()
        if enew == 0:
            return True, k + 1
        if P(e, enew, t) > random.uniform(0, 1):
            s = snew
    return (enew == 0), k + 1

@timeit
def BEAM(initial_state, h, beam_num, max_iters):
    beams = [initial_state] * beam_num
    for i in range(10):
        beams = [random.choice(beam.successors()) for beam in beams]
    for i in range(max_iters):
        beams = [min(beam.successors(), key=(
            lambda s: getattr(s, h)())) for beam in beams]
        done = [getattr(b, h)() == 0 for b in beams]
        if any(done):
            return True, (i + 1) * beam_num
    return False, (i + 1) * beam_num