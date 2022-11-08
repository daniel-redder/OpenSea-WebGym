from typing import Callable
import importlib



domain_name_list = {
    "connect_four_temp":"domains.connect_four_temp"
}


def getDomainNameList():
    return domain_name_list


def getConstructor(domainName):
    try:
        con = importlib.import_module(domain_name_list[domainName]).env
        return con


    except Exception as e:
        print(e)
        return False