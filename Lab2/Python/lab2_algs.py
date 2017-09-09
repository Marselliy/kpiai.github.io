import time

def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        return result + (te - ts,)

    return timed

@timeit
def BFS(initial_state):
    steps = 0
    import queue
    q = queue.Queue()
    initial_state.reset_marking()
    q.put(initial_state)
    
    while q.not_empty:
        state = q.get()
        steps += 1
        if state.solved():
            return True, steps
        state.mark()
        [q.put(s) for s in state.successors() if not(s.is_marked())]
    return False, steps
@timeit
def LDFS(state, depth, limit):
    steps = 0
    if depth < limit:
        steps += 1
        if state.solved():
            return True, steps
        for s in state.successors():
            flag, next_steps, _ = LDFS(s, depth + 1, limit)
            steps += next_steps
            if flag:
                return True, steps
    return False, steps
@timeit
def IDS(state):
    lim = 0
    steps = 0
    flag = False
    while not flag:
        flag, next_steps, _ = LDFS(state, 0, lim)
        steps += next_steps
        lim += 1
    return True, steps
@timeit
def RBFS(initial_state, heuristic):
    initial_state.reset_marking()
    steps = 0
    states = [initial_state]
    initial_cost = getattr(initial_state, heuristic)()
    
    while len(states) > 0:
        best_state = min(states, key=(
            lambda s: getattr(s, heuristic)()
        ))
        states.remove(best_state)
        steps += 1
        if best_state.solved():
            return True, steps
        best_state.mark()
        [states.append(s) for s in best_state.successors() if not(s.is_marked())]
    return False, steps
@timeit
def A_star(initial_state, heuristic):
    initial_state.reset_marking()
    steps = 0
    states = [initial_state]
    initial_cost = getattr(initial_state, heuristic)()
    
    while len(states) > 0:
        best_state = min(states, key=(
            lambda s: abs(initial_cost - getattr(s, heuristic)()) +
            getattr(s, heuristic)()
        ))
        states.remove(best_state)
        steps += 1
        if best_state.solved():
            return True, steps
        best_state.mark()
        [states.append(s) for s in best_state.successors() if not(s.is_marked())]
    return False, steps