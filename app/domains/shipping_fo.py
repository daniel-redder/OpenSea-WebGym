from pettingzoo import AECEnv
from gymnasium import spaces
from pettingzoo.utils.agent_selector import agent_selector
import numpy as np

class raw_env(AECEnv):
  metadata = {}
  
  def __init__(self,agent_count:int,move_speed=2,avg_route_len=100,route_count=10,avg_piracy=0.1,freq_storm=0.5,avg_storm=.4):
    super().__init__()
    # agent setup
    self.agents = [f"captain_{x}" for x in range(agent_count)]
    self.possible_agents = self.agents[:]
    self._cumulative_rewards = {f"captain_{x}":0.0 for x in range(agent_count)}
    self.move_speed = move_speed

    # environment setup
    self.avg_route_len = avg_route_len
    self.route_count = route_count
    self.avg_piracy = avg_piracy
    self.freq_storm = freq_storm
    self.avg_storm = avg_storm
    
    """
    change_route: index of route+1 or 0 for remain
    brace_for_pirates: 0 (don't brace and ship moves normally) 1 (brace and ship slows)
    """
    self.action_spaces = {
      i: spaces.Discrete(4)
      # spaces.Dict(
      #   {
      #     "route": spaces.Discrete(2),
      #     "brace": spaces.Discrete(2)
      #   }
      #)
       for i in self.agents
    }

    """
    flotsam:bool (curr route)
    route_length:int
    current_distance_traveled:int
    storms_passed_on_route:int
    """
    self.observation_spaces = {
      i: spaces.Dict(
        {
          "observation": spaces.Dict(
            {
              "route": spaces.Discrete(route_count),
              "dist": spaces.Discrete(int(avg_route_len + avg_route_len * 0.15 * 4)),
              "step": spaces.Discrete(int((avg_route_len + avg_route_len * 0.15 * 4) * 2)),
              "flotsam": spaces.Discrete(2),
              "storm": spaces.Discrete(2)
            }
          )
          # spaces.Dict(
          #   {
          #     "route": spaces.Discrete(2),
          #     "brace": spaces.Discrete(2)
          #   }
          # )
        }
      ) for i in self.agents
    }

    self.reset()
    
  def reset(self, seed=0, return_info=True, options={"options":1}):
    self.agents = self.possible_agents[:]
    self.rewards = {i: 0 for i in self.agents}
    self._cumulative_rewards = {name: 0 for name in self.agents}
    self.truncations = {i: False for i in self.agents}
    self.terminations = {i: False for i in self.agents}
    self.terminated = {i: False for i in self.agents}
    self.infos = {i: {} for i in self.agents}
    self._agent_selector = agent_selector(self.agents)
    self.agent_selection = self._agent_selector.reset()

    np.random.seed(seed)

    # list of :routes: (len of each route,piracy chance per tick, storm chance per tick)
    self.routes = [(int(np.random.normal(loc=self.avg_route_len, scale=0.15*self.avg_route_len)), np.random.normal(loc=self.move_speed/self.avg_route_len*self.avg_piracy,scale=0.35*self.move_speed/self.avg_route_len*self.avg_piracy), True if np.random.random() < self.freq_storm else False, np.random.normal(loc=self.move_speed/self.avg_route_len*self.avg_storm,scale=0.35*self.move_speed/self.avg_route_len*self.avg_storm)) for x in   range(self.route_count)]

    # flotsam count per route
    self.flotsam = [0 for i in self.routes]
    self.flotsam_lifetime = 10
    self.flotsam_ttl = self.flotsam_lifetime

    #The position of all agents (current route, distance along route, number of steps)
    self.state_space = [[int(np.random.random()*len(self.routes)), 0, 0] for i in self.agents]
    
  def observe(self, agent):
    return {
      "observation": {
        "route": self.state_space[self.agents.index(agent)][0],
        "dist": self.state_space[self.agents.index(agent)][1],
        "step": self.state_space[self.agents.index(agent)][2],
        "flotsam": 1 if self.flotsam[self.state_space[self.agents.index(agent)][0]] > 0 else 0,
        "storm": 1 if self.routes[self.state_space[self.agents.index(agent)][0]][2] else 0
      }
    }

  def observation_space(self, agent):
    return self.observation_spaces[agent]
  
  def action_space(self, agent):
    return self.action_spaces[agent]

  def step(self, action):

    # handle per-turn events
    if self.agents.index(self.agent_selection) == 0:
      # flotsam decay
      if self.flotsam_ttl == 0:
        for i in self.flotsam:
          i = 0 if i <= 0 else i - 1
        self.flotsam_ttl = self.flotsam_lifetime
      else:
        self.flotsam_ttl -= 1

    # handle per-ship actions
    if not self.terminated[self.agent_selection]:
      
      # active ship
      if self.truncations[self.agent_selection] or self.terminations[self.agent_selection]:
        return self._was_dead_step(action)

      ship = self.agent_selection
      ship_index = self.agents.index(ship)
      
      #print(ship+" a="+str(action))
      change_route = action%2
      brace = action/2
      
      # determine route progress
      self.state_space[ship_index][2] += 1
      if change_route:
        self.state_space[ship_index][0] = (self.state_space[ship_index][0] + 1) % len(self.routes)
      else:
        if brace:
          self.state_space[ship_index][1] += int(self.move_speed / 2)
        else: 
          self.state_space[ship_index][1] += int(self.move_speed)
          
      # check if theres storm damage
      if self.routes[self.state_space[ship_index][0]][2] and np.random.random() < self.routes[self.state_space[ship_index][0]][3]:
          self.flotsam[self.state_space[ship_index][0]] += 1

      # print(ship + " at " + str(self.state_space[ship_index][1] / self.state_space[ship_index][2] if self.state_space[ship_index][2] != 0 else 0))

      # check if there's a pirate attack
      if np.random.random() < self.routes[self.state_space[ship_index][0]][1] and not brace:
        self.flotsam[self.state_space[ship_index][0]] += 1
        self.rewards[ship] -= self.state_space[ship_index][2] / self.state_space[ship_index][1] if self.state_space[ship_index][1] != 0 else 0 # lose reward = -1*steps/dist
        # print(ship + " scored " + str(self.rewards[ship]))
        self.terminated[ship] = True
        self.terminations[ship] = True

      # check if route has been completed
      if self.routes[self.state_space[ship_index][0]][0] < self.state_space[ship_index][1]:
        self.rewards[ship] += self.state_space[ship_index][1] / self.state_space[ship_index][2] if self.state_space[ship_index][2] != 0 else 0 # win reward = dist/steps
        # print(ship + " scored " + str(self.rewards[ship]))
        self.terminated[ship] = True
        self.terminations[ship] = True

    # inactive ship
    else:

      # check if done
      all_dead = True
      last_alive = None
      for i in self.terminated:
        if not i:
          all_dead = False
          last_alive = i
          break

      # terminate if done
      if all_dead:
        self.terminations = {i: True for i in self.agents}
        return self._was_dead_step(None)        

    self.agent_selection = self._agent_selector.next()

    # petting zoo reward function
    self._accumulate_rewards()

#class shipping_fo(domain):
#  def env():
