import numpy as np

fields = [
    np.array([
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1,  0,  0,  0,  0,  0,  0,  0,  0, -1],
        [-1,  0,  0,  0,  0,  0,  0,  0,  0, -1],
        [-1,  0,  0,  0,  0,  0,  0,  0,  0, -1],
        [-1,  0,  0,  0,  0,  0,  0,  0,  0, -1],
        [-1,  0,  0,  0,  0,  0,  0,  0,  0, -1],
        [-1,  0,  0,  0,  0,  0,  0,  0,  0, -1],
        [-1,  0,  0,  0,  0,  0,  0,  0,  0, -1],
        [-1,  0,  0,  0,  0,  0,  0,  0,  0, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    ]),
    np.array([
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1,  0,  0,  0,  0,  0,  0,  0,  0, -1],
        [-1,  0, -1, -1, -1, -1, -1, -1,  0, -1],
        [-1,  0, -1,  0,  0,  0,  0,  0,  0, -1],
        [-1,  0, -1,  0,  0,  0,  0, -1,  0, -1],
        [-1,  0, -1,  0,  0,  0,  0, -1,  0, -1],
        [-1,  0, -1,  0,  0,  0,  0, -1,  0, -1],
        [-1,  0, -1, -1,  0, -1, -1, -1,  0, -1],
        [-1,  0,  0,  0,  0,  0,  0,  0,  0, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    ]),
    np.array([
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
        [-1,  0, -1,  0,  0,  0, -1,  0,  0, -1],
        [-1,  0, -1,  0, -1,  0, -1,  0,  0, -1],
        [-1,  0, -1,  0, -1,  0, -1,  0,  0, -1],
        [-1,  0, -1,  0, -1,  0, -1,  0,  0, -1],
        [-1,  0, -1,  0, -1,  0, -1,  0,  0, -1],
        [-1,  0, -1,  0, -1,  0, -1,  0,  0, -1],
        [-1,  0, -1,  0, -1,  0, -1,  0,  0, -1],
        [-1,  0,  0,  0, -1,  0,  0,  0,  0, -1],
        [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    ]),
]

# 0 - empty
# 1 - dirt
# 2 - wall
class Environment:
    def __init__(self, agent, field_index, dirt_prob=0.005, log=False, seed=1337):
        np.random.seed(seed)
        field = np.copy(fields[field_index])
        self.field = field
        self.dirt_prob = dirt_prob
        self.agent = agent
        self.agent_x = 4
        self.agent_y = 4
        self.log = log
        self.activate_bump = None
        
    def is_dirty(self, x, y):
        return self.field[x, y] >= 1
    def is_wall(self, x, y):
        return self.field[x, y] == -1
    
    def apply_action(self, action):
        if not (self.activate_bump is None):
            self.activate_bump = None
        if action == 'suck':
            if self.field[self.agent_x, self.agent_y] > 0:
                self.field[self.agent_x, self.agent_y] -= 1
        if action == 'move_up':
            if self.is_wall(self.agent_x - 1, self.agent_y):
                self.activate_bump = 'top'
            else:
                self.agent_x -= 1
        if action == 'move_down':
            if self.is_wall(self.agent_x + 1, self.agent_y):
                self.activate_bump = 'bottom'
            else:
                self.agent_x += 1
        if action == 'move_left':
            if self.is_wall(self.agent_x, self.agent_y - 1):
                self.activate_bump = 'left'
            else:
                self.agent_y -= 1
        if action == 'move_right':
            if self.is_wall(self.agent_x, self.agent_y + 1):
                self.activate_bump = 'right'
            else:
                self.agent_y += 1
               
    def step(self):
        dirt = np.random.random([10, 10]) < self.dirt_prob
        self.field += (self.field >= 0) * dirt
        
        action = self.agent.activate_sensors(self.is_dirty(self.agent_x, self.agent_y), self.activate_bump)
        if self.log:
            print('Environment: agent decided to %s.\n' % action)
        self.apply_action(action)
        return self.get_image()
    
    def get_image(self):
        field = np.copy(self.field)
        field[self.agent_x, self.agent_y] = -2
        return field