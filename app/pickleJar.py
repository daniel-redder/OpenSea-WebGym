import random
import sqlite3 as sql
import secrets
import os
from domains.domain import domainWrapper
import dill as pickle
from typing import Union, Any
import supersuit as ss


#the number of agents kept in memory
AGENT_CACHE_LIMIT= 1

#using LRU for caching

#optimize with lookup table?
global agent_cache
agent_cache = []

global agent_lookup
agent_lookup = []


global envID_ticker
envID_ticker = 0





if os.path.exists("ticker.txt"):
    with open("ticker.txt","r") as tick:
        envID_ticker = int(tick.readline())


def _getEnvID():
    global envID_ticker
    envID_ticker+=1
    return envID_ticker



from domains.connect_four_temp import raw_env as env
#TODO temporary remove
testenv = env()

agent_cache = []



def get_cache():
  return [ [md[1].uniqueName,md[1].envID,"",md[1].agentIndex,md[1].creationDate.strftime("%m/%d/%y, %H:%M"),str(md[1].trackingRewards)] for md in agent_cache]



def clear_cache():
    """

    :return:
    """
    for x in agent_cache:
        _saveModel(x)




def _saveModel(domain:[str,domainWrapper]):
    """

    :param domain:
    :return:
    """
    pass
    #TODO temporary bypass ss breaks this
    # with open("domains/data/"+domain[0]+".pkl","wb") as f:
    #     pickle.dump(domain[1],f)


def _loadModel(domainPathName:str)->domainWrapper:
    """

    :param domainPathName:
    :return:
    """
    with open("domains/data/"+domainPathName+".pkl","rb") as f:
        return pickle.load(f)



def _cache(domain):
    """
    holds the model in memory (to avoid uneccesary reads)

    [
    domainName_envId,{"domain":DOMAIN OBJECT, "agents":[agent API Keys]}
    ]

    :param agents:
    :return: None
    """

    key = f"{domain.uniqueName}_{domain.envID}"


    agent_cache.append([key,domain])
    agent_lookup.append(key)


    while(len(agent_cache) > AGENT_CACHE_LIMIT):
        removal_model = agent_cache.pop(0)
        agent_lookup.pop(0)
        _saveModel(removal_model)

#TODO
def _recache(domain:[str,domainWrapper]):
    """
    modifies order of cache (threaded)

    :return:
    """
    agent_cache.insert( 0, agent_cache.pop( agent_cache.index(domain) ) )
    agent_lookup.insert( 0, agent_lookup.pop(agent_lookup.index(domain[0])))
    #https://stackoverflow.com/questions/3173154/move-an-item-inside-a-list






def createInstance(domainName:str, agentCount:int, domain)->[str,[str]]:
    """
    Creates a new instance of a domain in Sqlite and generates API keys

    :param domainName:
    :param agentCount:
    :return: [envID, [agent API keys]]
    """
    apikeys = [str(secrets.token_urlsafe(5)) for x in range(agentCount)]


    envID = f"{_getEnvID()}{random.randint(1,1000)}"

    domain = domainWrapper(
        domain = domain,
        envID = envID,
        agentAPI= apikeys
    )


    #when first saved models are cached
    _cache(domain = domain )

    return  envID, apikeys




# def removeInstance(domainName, envId):
#     """
#     Removes a specific instance from the database
#
#     :param domainName:
#     :param envId:
#     :return:
#     """
#     pass
#     #agent_cache.remove()


def saveEnv(envID:str, domainName:str, domain):

    key = f"{domainName}_{envID}"

    try:
        exists = agent_lookup.index(key)

        agent_cache[exists][1] = domain
        _recache([key,domain])

    except:
        _cache(domain)



def getInstance(envID:str, domainName:str, apiKey:str)->Union[bool,Any]:
    """

    :param envID:
    :param domainName:
    :param apiKey:
    :return:
    """

    key = f"{domainName}_{envID}"
    # print(key)
    # print(agent_lookup)

    for x in agent_lookup:
        print(agent_cache[agent_lookup.index(x)][1].agentAPI,x)


    try:
        exists = agent_lookup.index(key)
        #exists = agent_cache

        print(type(agent_cache[exists][1]))
        print(agent_cache[exists][1].agentAPI)
        #handles faulty apiKey
        # if not apiKey in agent_cache[exists][1].agentAPI:
        #     return False

        #TODO
        #threading here to edit position in memory stack
        _recache(agent_cache[exists])

        return agent_cache[exists][1]


    except Exception as e:
        print(e, "  expected ")

        domain=_loadModel(key)

        #TODO
        #thread
        _cache(domain)

        if not apiKey in domain.agentAPI:
            return False

        return domain[1]