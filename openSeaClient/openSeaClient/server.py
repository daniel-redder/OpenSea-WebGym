

class server():

    def __init__(self, ipaddr:str, port:int=80):
        self.ipaddr = ipaddr
        self.port = port

        self.test_connection()


    def test_connection(self):
        """
        attempts to connect to the server with given specifications
        :return:
        """


    def create_env(self):
        """
        calls model creation
        :return:
        """
        pass


    def model_connect(self,):
        """
        connects to existing environment
        :return:
        """



    def step(self):
        """
        sends step to environment and returns results
        :return:
        """
        pass


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