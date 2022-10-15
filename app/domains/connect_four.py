from pettingzoo.classic import connect_four_v3 as cf
from domain import domain


class connect_four(domain):

    def __init__(self,**args):
        
    #new = connect_four(pinball_bool=False)
    #args = {"pinball_bool":False}
      
      super(domain,self)
      self.model = cf.env()



test = connect_four(**args)
test.model.reset()

print(test.model.agents)
print(test.model.max_num_agents)