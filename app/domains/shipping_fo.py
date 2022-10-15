from domain import domain
from pettingzoo import AECEnv
from gymnasium import spaces
import numpy as np

class raw_env(AECEnv):
  metadata = {}
  
  def __init__(self,avg_route_len=100,route_count=None,avg_piracy=0.1,pStorm=[.4]):
    super().__init__()
    
    self.agents = None

    self.move_speed=2

    np.random.seed(seed = self.seed)

    self.route_count = route_count or int(np.random.normal(loc=6,std=3))

      #list of :routes: (len of each route,piracy chance per tick)
    self.routes = [(int(np.random.normal(loc=avg_route_len, std=0.15*avg_route_len)),np.random.normal(loc=self.move_speed/avg_route_len*avg_priacy, std=0.35*self.move_speed/avg_route_len*avg_priacy)) for x in   range(self.route_count)]

    self.flotsam = [[0 for x in range(y[0])] for y in self.routes]


    for route in range(len(self.routes)):
      for storm_index in range():
      if storm_index>=len(pStorm):
        
      
      
      elif np.random.random()>pStorm[storm_index]:
        self.flotsam[route][np.random.randint(low=0,high=self.routes[route][0]-1)] = 1
        storm_index+1
    
    
    """
    sail_forward (implicit?)
    change_route: index of route+1 or 0 for remain
    brace_for_pirates: 0 (don't brace and ship moves normally) 1 (brace and ship slows)
    """
    
    self.action_spaces = None


    """
    flotsam:bool (curr route)
    route_length:int
    current_distance_traveled:int
    storms_passed_on_route:int
    """
    self.observation_spaces = {
      i:spaces.Dict({
        #pause
      })
      for i in self.agents
    }


    self.state_space = 


  

  def reset(self):
    pass



  def step(self):

    if (
            self.truncations[self.agent_selection]
            or self.terminations[self.agent_selection]
      ):
            return self._was_dead_step(action)


  def observe(self):
        



class shipping_fo(domain):
  def env():



