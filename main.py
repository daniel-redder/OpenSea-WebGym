from pettingzoo.test import api_test 
from app.domains.shipping_fo import raw_env as shipping_fo
from app.domains.connect_four_temp import raw_env as c4
import numpy

env = shipping_fo(8)
#env = c4()
#api_test(env, num_cycles=100, verbose_progress=False)




env.reset()

results = {agent:{"observations":[],"terminations":[],"truncations":[],"rewards":[]} for agent in env.agents}

for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()
    #print(observation,reward,termination,truncation,info,agent)
    #action = policy(observation, agent)
    action = numpy.random.randint(4) if env.terminations[agent] == False and env.truncations[agent] == False else None #shipping_fo
    # if env.terminations[agent] == False:
    #     action = numpy.random.randint(7) if env.terminations[agent] == False else None #c4
    #     for action in range(7):
    #         if observation["action_mask"][action] == 1:
    #             break
    # else:
    #     action = None
    env.step(action)

    if env.terminated[agent]:
        results[agent]["rewards"].append(reward)
        results[agent]['observations'].append(observation)
        results[agent]['terminations'].append(termination)
        results[agent]['truncations'].append(truncation)

    # if agent == "captain_0":
    #     print("\n STEP " + str(env.state_space[int(agent[-1])][2]), agent if termination == False else "*", end=", ")
    # else:
    #     print(agent if termination == False else "*", end=", ")

print("\n")
for agent in results:
    print(agent,results[agent])