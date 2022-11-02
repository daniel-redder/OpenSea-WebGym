from datetime import datetime

class domainWrapper():
    def __init__(self,envID:str,agentAPI:[str],domain,agentIndex:int=0,uniqueName:str=None,trackingRewards:bool=False):
        """
        Instantiates a domain.
        :param uniqueName:

        """
        self.domain = domain
        self.uniqueName = uniqueName or domain.metadata['name']

        self.envID = envID
        self.agentAPI = agentAPI,
        self.agentIndex = 0

        self.creationDate = datetime.now() #test loading

        self.trackingRewards = trackingRewards
      

