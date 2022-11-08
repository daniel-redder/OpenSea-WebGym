# from pettingzoo.test import api_test
# from app.domains.shipping_fo import raw_env as shipping_fo
# from app.domains.connect_four_temp import raw_env as c4
# import numpy
#
# env = shipping_fo(8)
# #env = c4()
# #api_test(env, num_cycles=100, verbose_progress=False)
#
# env.reset()
# for agent in env.agent_iter():
#     observation, reward, termination, truncation, info = env.last()
#     print(observation,reward,termination,truncation,info,agent)
#     #action = policy(observation, agent)
#     action = {"route":0, "brace":0} if env.terminations[agent] == False else None #shipping_fo
#     #action = numpy.random.randint(0,6) if env.terminations[agent] == False else None #c4
#     env.step(action)


#FOR parallell from towards data science
# from ray import tune
# from ray.rllib.models import ModelCatalog
# from ray.rllib.models.torch.torch_modelv2 import TorchModelV2
# from ray.tune.registry import register_env
# from ray.rllib.env.wrappers.pettingzoo_env import ParallelPettingZooEnv
# from pettingzoo.butterfly import pistonball_v5
# import supersuit as ss
# import torch
# from torch import nn


from stable_baselines3.ppo import CnnPolicy
from stable_baselines3 import PPO
from pettingzoo.butterfly import pistonball_v5

import supersuit as ss


from digZooClient.digZooClient.server import server


env = server(ipaddr="127.0.0.1",port=8080)

wrap = lambda x: ss.color_reduction_v0(x,mode='B')

val=env.create_env(domainName="piston",ss_wrapper=wrap,n_pistons=20, time_penalty=-0.1,
                   continuous=True, random_drop=True, random_rotate=True,
                   ball_mass=0.75, ball_friction=0.3, ball_elasticity=1.5,
                   max_cycles=125)
print(val)

env.modelConnect(apiKeys=val["agent_api_keys"])

looper = True
while looper:
    curr_agent = env.agent_wait()

    if curr_agent == False:
        looper = False
        break

    observation, reward, done, info = env.last(curr_agent)
    action =

