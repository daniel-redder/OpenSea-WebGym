import sqlite3 as sql
import secrets
import os
from domains.domain import domainWrapper
import dill as pickle
from typing import Union, Any



#the number of agents kept in memory
AGENT_CACHE_LIMIT= 3

#using LRU for caching

#optimize with lookup table?
global agent_cache
agent_cache = {}

global agent_queue
agent_queue = []

global envID_ticker
envID_ticker = 0


if os.path.exists("ticker.txt"):
    with open("ticker.txt","r") as tick:
        envID_ticker = int(tick.readline())


def _getEnvID():
    envID_ticker+=1
    return envID_ticker



def _saveModel(domain:[str,domainWrapper]):
    """

    :param domain:
    :return:
    """
    pickle.dump(domain[1],"data/"+domain[0])


def _loadModel(domainPathName:str)->domainWrapper:
    """

    :param domainPathName:
    :return:
    """
    return pickle.load("data/"+domainPathName)



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


    while(len(agent_cache) > AGENT_CACHE_LIMIT):
        removal_model = agent_cache.pop(0)
        _saveModel(removal_model)

#TODO
def recache():
    """
    modifies order of cache (threaded)

    :return:
    """
    pass







def createInstance(domainName:str, agentCount:int, domain)->[str,[str]]:
    """
    Creates a new instance of a domain in Sqlite and generates API keys

    :param domainName:
    :param agentCount:
    :return: [envID, [agent API keys]]
    """
    apikeys = [str(secrets.token_urlsafe(5)) for x in range(agentCount)]


    envID = _getEnvID()

    domain = domainWrapper(
        domain = domain,
        envID = envID,
        agentIndex=0,
        agentAPI= apikeys
    )


    #when first saved models are cached
    _cache(domain = domain )

    return  envID, apikeys




def removeInstance(domainName, envId):
    """
    Removes a specific instance from the database

    :param domainName:
    :param envId:
    :return:
    """
    pass
    #agent_cache.remove()



def getInstance(envID:str, domainName:str, apiKey:str)->Union[bool,Any]:
    """

    :param envID:
    :param domainName:
    :param apiKey:
    :return:
    """

    key = f"{domainName}_{envID}"

    try:
        exists = agent_cache[key]

        #handles faulty apiKey
        if not apiKey in agent_cache[exists].agentAPI:
            return False

        #TODO
        #threading here to edit position in memory stack
        recache()

        return agent_cache[exists]


    except:

        domain=_loadModel(key)

        #TODO
        #thread
        _cache(domain)

        if not apiKey in domain.agentAPI:
            return False

        return domain