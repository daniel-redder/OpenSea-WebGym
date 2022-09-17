import gym


class domain(gym.Env):
    def __init__(self,uniqueName:str):
        """
        Instantiates a domain.
        :param uniqueName:

        """

        self.env_id = None
        self.uniqueName = uniqueName


    def get_agent_api(self)->[int]:
        return None