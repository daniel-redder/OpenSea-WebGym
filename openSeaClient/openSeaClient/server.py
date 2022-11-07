import requests

class server():

    def __init__(self, ipaddr:str=None, port:int=80):
        self.ipaddr = ipaddr
        self.port = port
        self.test_connection()

        #-------------- given by remote (or config) ----------------
        self.apiKeys = None
        self.envID = None
        self.domainName = None
        #-----------------------------------------------

    def test_connection(self):
        """
        attempts to connect to the server with given specifications
        :return:
        """

        try:
            val = requests.post(self.ipaddr+self.port+"/ping",json={})
            print(val)
        except:
            print("connection failure")


    def create_env(self,domainName,agentCount,**args):
        """
        calls model creation
        :return:
        """
        url = f"{self.ipaddr}:{self.port}/env/createzoo/{domainName}"
        args["agentCount"] = agentCount

        try:
            val = requests.post(url, json=args)
            self.domainName = domainName
            return val

        except:
            print("Environment Creation Failure")






    def step(self,action,agentIndex):
        """
        sends step to environment
        :return:
        """
        url = f"{self.ipaddr}:{self.port}/env/stepzoo/{self.domainName}/{self.envID}/{self.apiKeys[agentIndex]}"
        json = {"action":action}

        try:
            val = requests.post(url,json=json)
        except:
            print("failure on step")


    def wait(self,ping_test_delay:int):
        """
        waits for turn to act
        :param ping_test_delay:
        :return:
        """
        pass

    def reset(self):
        """
        resets environment
        :return:
        """
        pass