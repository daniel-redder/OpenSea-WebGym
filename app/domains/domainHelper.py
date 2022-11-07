from typing import Callable




domain_name_list = {
    "connect_four_temp"
}



def getConstructor(domainName):
    try:
        con = __import__(domain_name_list[domainName]).env
        return con


    except:
        return False