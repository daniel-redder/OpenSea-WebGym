from .domain import domainWrapper
from typing import Callable




domain_name_list =[

]





def getDomainNameList()->[str]:
    return domain_name_list


def getConstructor(domainName)->Callable[...,domainWrapper]:
    return