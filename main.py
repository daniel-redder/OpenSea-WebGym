from pettingzoo.test import api_test 
from app.domains.shipping_fo import raw_env as shipping_fo
from app.domains.connect_four_temp import raw_env as c4
import numpy

env = shipping_fo(8)
#env = c4()
api_test(env, num_cycles=100, verbose_progress=True)

# env.reset()
# for agent in env.agent_iter():
#     observation, reward, termination, truncation, info = env.last()
#     print(observation,reward,termination,truncation,info,agent)
#     #action = policy(observation, agent)
#     action = numpy.random.randint(4) if env.terminations[agent] == False and env.truncations[agent] == False else None #shipping_fo
#     #action = numpy.random.randint(7) if env.terminations[agent] == False else None #c4
#     env.step(action)