from datetime import datetime

class domainWrapper():
    def __init__(self,envID:str,agentAPI:[str],domain,uniqueName:str=None,trackingRewards:bool=False):
        """
        Instantiates a domain.
        :param uniqueName:

        """
        self.domain = domain
        self.uniqueName = uniqueName or domain.metadata['name']
        self.isDone = False
        self.envID = envID
        self.agentAPI = agentAPI

        self.agentMap = {str(self.domain.agents[i]):self.agentAPI[i] for i in range(len(self.domain.agents))}
        self.agentIterable = iter(domain.agent_iter())
        self.stepAEC()

        self.creationDate = datetime.now() #test loading

        self.trackingRewards = trackingRewards


    def stepAEC(self):
        try:
            self.currAgent = next(self.agentIterable)
            return False
        except:
            self.isDone = True
            return True

    def reset(self):
        self.isDone = False
        self.agentIterable = iter(self.domain.agent_iter())
        self.stepAEC()

