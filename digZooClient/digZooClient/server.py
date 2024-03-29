import time
import supersuit as ss
import requests
import dill as pickle
import jsonpickle
import jsonpickle.ext.numpy as jsonpickle_numpy

jsonpickle_numpy.register_handlers()

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


    def _request(self,url,json=None,error="standard connection error"):
        try:
            if json is None: return requests.post(url="http://"+url).json()
            return requests.post(url="http://"+url,json=json).json()
        except Exception as e:
            print(error, e)
            print(f"{url}, {json}")
            assert False, "error on request"

    def test_connection(self):
        """
        attempts to connect to the server with given specifications
        :return:
        """
        url = f"{self.ipaddr}:{self.port}/ping"

        val = self._request(url)
        #print(val)



    def create_env(self,domainName,ss_wrapper=None,agentCount=None,**args):
        """
        calls model creation
        :return:
        """
        url = f"{self.ipaddr}:{self.port}/env/createzoo/{domainName}"
        if args is None:
            args = {}

        if not agentCount is None:
            args["agentCount"] = agentCount

        if ss_wrapper is None:
            val = self._request(url,args)
            self.domainName = domainName
            return val
        else:
            val = self._request(url, args)
            self.domainName = domainName
            with open(f"{domainName}_{val['env_id']}.pkl","wb") as f:
                pickle.dump(ss_wrapper,f)

            url = f"{self.ipaddr}:{self.port}/env/supersuit/{domainName}/{val['env_id']}/{val['agent_api_keys'][0]}"
            file_path = f"{domainName}_{val['env_id']}.pkl"

            with open(file_path,"rb") as file:
                check = requests.post(url = "http://"+url, files={"file":file})

            return val




    def modelConnect(self,apiKeys:[str],domainName:str=None, envID=None):
        if domainName is None: domainName = self.domainName
        else: self.domainName = domainName
        if envID is None: envID = self.envID
        else: self.envID = envID
        self.apiKeys = apiKeys


        url = f"{self.ipaddr}:{self.port}/env/configzoo/{self.domainName}/{envID}"

        json = {"apikeys":apiKeys}


        val = self._request(url,json)
        self.agentMap= {val["agents"][i]:apiKeys[i] for i in range(len(apiKeys))}
        self.agents = [x for x in self.agentMap]







    def step(self,action,agent):
        """
        sends step to environment
        :return:
        """
        url = f"{self.ipaddr}:{self.port}/env/stepzoo/{self.domainName}/{self.envID}/{self.agentMap[agent]}"
        json = jsonpickle.encode(action)


        val = self._request(url,json)

        if "done" in val:
            return True
        return False



    def last(self,agent):
        url = f"{self.ipaddr}:{self.port}/env/lastzoo/{self.domainName}/{self.envID}/{self.agentMap[agent]}"


        val = self._request(url)
        #print(val)
        #return val.obs, val.rew, val.term, val.trunc, val.info

        #print(jsonpickle.decode(val["observation"]))
        #print("0-------")

        return jsonpickle.decode(val["observation"]), val["reward"], val["termination"], val["truncation"], val["info"]




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
                val=self._request(url,json)

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
            val = self._request(url,json)
        except:
            print("error in reset")