import time

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


    def modelConnect(self,apiKeys:[str],domainName:str=None, envID=None):
        if domainName is None: domainName = self.domainName
        else: self.domainName = domainName
        if envID is None: envID = self.envID
        else: self.envID = envID
        self.apiKeys = apiKeys


        url = f"{self.ipaddr}:{self.port}/env/configzoo/{self.domainName}/{self.envID}"

        json = {"apiKeys":apiKeys}

        try:
            val = requests.post(url,json=json)
            self.agentMap= {val["agents"][i]:apiKeys[i] for i in range(len(apiKeys))}
        except:
            print("agent api mapping failed")






    def step(self,action,agent):
        """
        sends step to environment
        :return:
        """
        url = f"{self.ipaddr}:{self.port}/env/stepzoo/{self.domainName}/{self.envID}/{self.agentMap[agent]}"
        json = {"action":action}

        try:
            val = requests.post(url,json=json)

        except:
            print("failure on step")


    def last(self,agent):
        url = f"{self.ipaddr}:{self.port}/env/lastzoo/{self.envID}/{self.agentMap[agent]}"
        json = {}

        try:
            val = requests.post(url,json=json)
            return val["observation"], val["reward"], val["termination"], val["truncation"], val["info"]
        except:
            print("last failure")



    def agent_wait(self,ping_test_delay:int=10):
        """
        waits for turn to act
        :param ping_test_delay:
        :return:
        """
        url = f"{self.ipaddr}:{self.port}/env/checkzoo/{self.domainName}/{self.envID}/{self.apiKeys[0]}"
        json = {}
        agent = ""
        while not agent in self.agents:
            try:
                val=requests.post(url,json=json)

                if "done" in val:
                    return False

                if val["agent"] in self.agentMap:
                    return val["agent"]
            except:
                print("failure to iter")

            time.sleep(ping_test_delay)






    def reset(self):
        """
        resets environment
        :return:
        """
        url = f"{self.ipaddr}:{self.port}/env/resetgym/{self.domainName}/{self.envID}/{self.apiKeys[0]}"
        json = {}

        try:
            val = requests.post(url, json=json)
        except:
            print("error in reset")