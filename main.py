from pettingzoo.test import api_test 
from app.domains.shipping_fo import raw_env as shipping_fo
from app.domains.connect_four_temp import raw_env as c4
import numpy

env = shipping_fo(100)
#env = c4()
#api_test(env, num_cycles=100, verbose_progress=False)

env.reset()
for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()
    #action = policy(observation, agent)
    action = {"route":0, "brace":0} if env.terminations[agent] == False else None #shipping_fo
    #action = numpy.random.randint(0,6) if env.terminations[agent] == False else None #c4
    env.step(action)