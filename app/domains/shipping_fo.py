from pettingzoo import AECEnv
from gymnasium import spaces
import numpy as np

class raw_env(AECEnv):
  metadata = {}
  
  def __init__(self,agent_count:int,avg_route_len=100,route_count=10,avg_piracy=0.1,avg_storm=.4):
    super().__init__()
    self.agent_count = agent_count
    self.avg_route_len = avg_route_len
    self.route_count = route_count
    self.avg_piracy = avg_piracy
    self.avg_storm = avg_storm
    reset()
    
  def reset(self):
    self.agents = [f"captain_{x}" for x in range(agent_count)]
    self.possible_agents = self.agents[:]

    self.move_speed=2

    np.random.seed(seed = 0)

    self.route_count = route_count or int(np.random.normal(loc=6,scale=3))

      #list of :routes: (len of each route,piracy chance per tick, storm chance per tick)
    self.routes = [(int(np.random.normal(loc=avg_route_len, scale=0.15*avg_route_len)), np.random.normal(loc=self.move_speed/avg_route_len*avg_piracy,scale=0.35*self.move_speed/avg_route_len*avg_piracy), np.random.normal(loc=self.move_speed/avg_route_len*avg_storm,scale=0.35*self.move_speed/avg_route_len*avg_storm)) for x in   range(self.route_count)]

    self.flotsam = [[0 for x in range(y[0])] for y in self.routes]    
    
    """
    change_route: index of route+1 or 0 for remain
    brace_for_pirates: 0 (don't brace and ship moves normally) 1 (brace and ship slows)
    """
    
    # self.action_spaces = None
    # action 0, action 1
    # ((0,1),(0,1))
    
    """
    flotsam:bool (curr route)
    route_length:int
    current_distance_traveled:int
    storms_passed_on_route:int
    """
    # self.observation_spaces = {
    #   i:spaces.Dict({
    #     #pause
    #   })
    #   for i in self.agents
    # }


    #The position of all agents (current route, distance along route, number of steps)
    
    self.state_space = [[int(np.random.random()*len(self.routes)), 0, 0] for x in self.agents]

  def step(self, action:[int]):

    if (
            self.truncations[self.agent_selection]
            or self.terminations[self.agent_selection]
      ):
            return self._was_dead_step(action)

    ship = self.agent_selection
    ship_index = self.agents.index(ship)
    
    change_route = action[0]
    brace = action[1]
    
    # determine route progress
    if change_route:
      self.state_space[ship_index][0] = (self.state_space[ship_index][0] + 1) % len(self.routes)
    else:
      if brace:
        self.state_space[ship_index][1] += self.move_speed / 2
      else: 
        self.state_space[ship_index][1] += self.move_speed
        
    # check if theres a storm
    if np.random.random() < self.routes[self.state_space[ship_index][0]][2]:
        self.flotsam[self.state_space[ship_index][0]] += 1
      
    # check if there's a pirate attack
    if np.random.random() < self.routes[self.state_space[ship_index][0]][1] and not brace:
        self.flotsam[self.state_space[ship_index][0]] += 1
        self.rewards[ship] -= ship.state_space[ship_index][2] / ship.state_space[ship_index][1] # lose reward = -1*steps/dist
        self.terminations[ship_index] = True

    # check if route has been completed
    if self.routes[ship.state_space[ship_index][0]][0] < ship.state_space[ship_index][1]:
      self.rewards[ship] += ship.state_space[ship_index][1] / ship.state_space[ship_index][2] # win reward = dist/steps
      self.terminations[ship_index] = True

    self.agent_selection = self._agent_selector.next()

    # petting zoo reward function
    self._accumulate_rewards()

  #def observe(self):

#class shipping_fo(domain):
#  def env():
