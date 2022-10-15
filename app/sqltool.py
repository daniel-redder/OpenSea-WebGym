import sqlite3 as sql
import secrets
import os
import dill as pickle

#database initialization for instance tracking -------------------------------------
conn = sql.connect("db.db")
curse = conn.cursor()

curse.execute(
    """
    CREATE TABLE IF NOT EXISTS Envs(
	envID INTEGER NOT NULL AUTOINCREMENT,
	domainName VARCHAR(20) UNIQUE NOT NULL,
	agentIndex INTEGER NOT NULL,
	agentAPIKey VARCHAR(12) NOT NULL,
	PRIMARY KEY (envID, domainName, agentIndex)
    );
    """
)
conn.commit()
curse.close()
conn.close()
#--------------------------------------------------------------------------------------

#the number of agents kept in memory
AGENT_CACHE_LIMIT= 3

#optimize with lookup table?
#agent_lookup_cache = {}
agent_cache = []

def cache(agents:[str], domain, envID:int, domainName:str):
    """
    holds the model in memory (to avoid uneccesary reads)

    [
    domainName_envId,{"domain":DOMAIN OBJECT, "agents":[agent API Keys]}
    ]

    :param agents:
    :return: None
    """
    for i in agents:
        agent_cache.append(i)

    while(len(agent_cache) > AGENT_CACHE_LIMIT):
        agent_cache.pop(0)


def connector()->[sql.Connection,sql.Cursor]:
    conn=sql.connect("db.db")
    curse = conn.cursor()
    return conn, curse


def createInstance(domainName:str, agentCount:int, domain)->[str,[str]]:
    """
    Creates a new instance of a domain in Sqlite and generates API keys

    :param domainName:
    :param agentCount:
    :return: [envID, [agent API keys]]
    """
    apikeys = [str(secrets.token_urlsafe(5)) for x in range(agentCount)]


    conn, curse = connector()

    for i in range(len(apikeys)):
        curse.execute(
            f"""
            INSERT INTO Envs(domainName, agentIndex, agentAPIKey) 
            VALUES({domainName}, {i}, {apikeys[i]})
            """)

    conn.commit()

    curse.execute(
        f"""
        SELECT envID
        FROM Envs
        WHERE domainName = {domainName} AND 
        agentIndex = {0}
        """
    )

    #TODO test for indexing problems here
    envID = curse.fetchall()[0][0]


    curse.close()
    conn.close()

    #when first saved models are cached
    cache(agents = apikeys, domain=domain, envID=envID, domainName=domainName)

    return  envID, apikeys




def removeInstance(domainName, envId):
    """
    Removes a specific instance from the database

    :param domainName:
    :param envId:
    :return:
    """
    conn, curse = connector()
    curse.execute(
        f"""
        REMOVE FROM Envs
        WHERE domainName = {domainName} AND envID = {envId};
        """
    )
    conn.commit()
    curse.close()
    conn.close()

    try:
        os.remove(f"domain_pickle/{domainName}_{envId}")
    except Exception as e:
        print(e, f"tried to remove environment, but failed, {domainName}_{envId}")



#TODO naively searching improve with some variant of lookup table
def getInstance(envID:str, domainName:str):

    key = f"{domainName}_{envID}"

    if key in

    else:
        model = pickle.load(f"domain_pickle/{domainName}_{envID}")
