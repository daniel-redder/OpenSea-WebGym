

class domainWrapper():
    def __init__(self,envID:str,agentAPI:[str],agentIndex:int,domain,uniqueName:str=None):
        """
        Instantiates a domain.
        :param uniqueName:

        """
        self.domain = domain
        self.uniqueName = uniqueName or str(domain.__class__)

        self.envID = envID
        self.agentAPI = agentAPI,
        self.agentIndex = agentIndex

