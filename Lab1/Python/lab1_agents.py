import numpy as np

class ReflexAgent:
    def __init__(self, rules, init_energy=2000, log=False, seed=1):
        np.random.seed(seed)
        self.rules = dict(rules)
        for sense in self.rules.keys():
            self.rules[sense] = getattr(self, self.rules[sense])
        self.energy = init_energy
        self.log = log
        
    def move_random(self, forbidden_direction):
        choices = []
        if 'left' != forbidden_direction:
            choices.append('move_left')
        if 'top' != forbidden_direction:
            choices.append('move_up')
        if 'right' != forbidden_direction:
            choices.append('move_right')
        if 'bottom' != forbidden_direction:
            choices.append('move_down')
        direction = np.random.choice(choices)
        return direction
    def move_up(self, sense):
        return 'move_up'
    def move_down(self, sense):
        return 'move_down'
    def move_left(self, sense):
        return 'move_left'
    def move_right(self, sense):
        return 'move_right'
    def idle(self, sense):
        return 'idle'
    def suck(self, sense):
        return 'suck'
    
    def activate_sensors(self, dirty, bump):
        if self.log:
            message = 'Agent sensors: '
            if dirty:
                message += 'dirty'
            if not (bump is None):
                message += ' bump from %s' % bump
            print(message)
        if self.energy < 2:
            return self.idle()
        sense = ''
        if dirty:
            sense += '_dirty'
        if not(bump is None):
            sense += ('_' + bump)
            
        # Apply rule
        return self.rules[sense[1:]](sense)
    
    
    
    
    
class ReflexModelAgent:
    def __init__(self, rules, init_energy=2000, log=False, seed=1):
        np.random.seed(seed)
        self.rules = dict(rules)
        for sense in self.rules.keys():
            self.rules[sense] = getattr(self, self.rules[sense])
        self.energy = init_energy
        self.log = log
        
        self.last_action = ''
        
    def move_random(self, forbidden_direction):
        choices = []
        if 'left' != forbidden_direction:
            choices.append('move_left')
        if 'top' != forbidden_direction:
            choices.append('move_up')
        if 'right' != forbidden_direction:
            choices.append('move_right')
        if 'bottom' != forbidden_direction:
            choices.append('move_down')
        if len(choices) > 1 and self.last_action in choices:
            choices.remove(self.last_action)
        direction = np.random.choice(choices)
        return direction
    def move_up(self, sense):
        return 'move_up'
    def move_down(self, sense):
        return 'move_down'
    def move_left(self, sense):
        return 'move_left'
    def move_right(self, sense):
        return 'move_right'
    def idle(self, sense):
        return 'idle'
    def suck(self, sense):
        return 'suck'
    
    def activate_sensors(self, dirty, bump):
        if self.log:
            message = 'Agent sensors: '
            if dirty:
                message += 'dirty'
            if not (bump is None):
                message += ' bump from %s' % bump
            print(message)
        if self.energy < 2:
            return self.idle()
        sense = ''
        if dirty:
            sense += '_dirty'
        if not(bump is None):
            sense += ('_' + bump)
            
        # Apply rule
        action = self.rules[sense[1:]](sense)
        self.last_action = action
        return action