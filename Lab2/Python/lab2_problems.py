import numpy as np
import random
from functools import reduce

import numpy as np
import random
from functools import reduce

class EightPuzzleState():
    
    goal = [i for i in range(8,-1,-1)]
    
    def __init__(self, field=goal):
        self.field = field
        self.cost_h1 = None
        self.cost_h2 = None
        
    def random_state(self, swaps=20):
        states = [EightPuzzleState(EightPuzzleState.goal)]
        for i in range(swaps + 1):
            worst_cost = max(states, key=(
                lambda s: s.h1()
            )).h1()
            worst_state = random.choice([s for s in states if s.h1() == worst_cost])
            states.remove(worst_state)
            states.extend(worst_state.successors())
        return worst_state
        
        
    def move_up(self):
        empty_pos = self.field.index(0)
        if empty_pos in [6, 7, 8]:
            return None
        new_field = self.field[:]
        new_field[empty_pos], new_field[empty_pos + 3] = new_field[empty_pos + 3], new_field[empty_pos]
        return EightPuzzleState(new_field)
    def move_down(self):
        empty_pos = self.field.index(0)
        if empty_pos in [0, 1, 2]:
            return None
        new_field = self.field[:]
        new_field[empty_pos], new_field[empty_pos - 3] = new_field[empty_pos - 3], new_field[empty_pos]
        return EightPuzzleState(new_field)
    def move_left(self):
        empty_pos = self.field.index(0)
        if empty_pos in [2, 5, 8]:
            return None
        new_field = self.field[:]
        new_field[empty_pos], new_field[empty_pos + 1] = new_field[empty_pos + 1], new_field[empty_pos]
        return EightPuzzleState(new_field)
    def move_right(self):
        empty_pos = self.field.index(0)
        if empty_pos in [0, 3, 6]:
            return None
        new_field = self.field[:]
        new_field[empty_pos], new_field[empty_pos - 1] = new_field[empty_pos - 1], new_field[empty_pos]
        return EightPuzzleState(new_field)
    
    def successors(self):
        return [state for state in [self.move_up(), self.move_down(), self.move_left(), self.move_right()] if state != None]
    
    def solved(self):
        return self.field == EightPuzzleState.goal
    
        
    @staticmethod
    def reset_marking():
        EightPuzzleState.marking = set()
    def is_marked(self):
        return tuple(self.field) in EightPuzzleState.marking
    def mark(self):
        EightPuzzleState.marking.add(tuple(self.field))
        
    def h1(self):
        if self.cost_h1 == None:
            self.cost_h1 = sum([EightPuzzleState.goal[i] != self.field[i] for i in range(9)])
        return self.cost_h1
    
    def h2(self):
        if self.cost_h2 == None:
            self.cost_h2 = sum([abs(EightPuzzleState.goal[i] - self.field[i]) for i in range(9)])
        return self.cost_h2
    
    def show(self):
        print("-------------")
        print("| %d | %d | %d |" % tuple(self.field[:3]))
        print("-------------")
        print("| %d | %d | %d |" % tuple(self.field[3:6]))
        print("-------------")
        print("| %d | %d | %d |" % tuple(self.field[6:]))
        print("-------------")
        
        
class EightQueensState():
    
    def __init__(self, field=np.arange(8).tolist()):
        self.field = field
        self.cost_f1 = None
        self.cost_f2 = None
        
    def random_state(self):
        field = np.arange(8)
        np.random.shuffle(field)
        return EightQueensState(field.tolist())
           
    def successors(self):
        return [EightQueensState(f) for f in reduce(lambda a,b: a + b,
                      [[(self.field[:index] + [n] + self.field[index+1:]) 
                        for n in range(8) if n != self.field[index]] 
                       for index in range(len(self.field))])]
    
    def solved(self):
        return self.f2() == 0
    
        
    @staticmethod
    def reset_marking():
        EightQueensState.marking = set()
    def is_marked(self):
        return tuple(self.field) in EightQueensState.marking
    def mark(self):
        EightQueensState.marking.add(tuple(self.field))
        
    def f1(self):
        if self.cost_f1 == None:
            self.cost_f1 = (np.unique(self.field, return_counts=True)[1] - 1).sum() + (
                np.unique(np.arange(8) - self.field, return_counts=True)[1] - 1).sum() + (
                np.unique(np.arange(7, -1, -1) - self.field, return_counts=True)[1] - 1).sum()
        return self.cost_f1
    
    def f2(self):
        if self.cost_f2 == None:
            hits = 0
            for i in range(len(self.field)):
                for j in range(i):
                    if self.field[i] == self.field[j]:
                        hits += 1
                        continue
                    if abs(i - j) == abs(self.field[i] - self.field[j]):
                        hits += 1
            self.cost_f2 = hits
        return self.cost_f2
    
    def show(self):
        for i in range(len(self.field)):
            row = '. ' * self.field[i] + '#' + ' .' * (len(self.field) - self.field[i] - 1)
            print(row)