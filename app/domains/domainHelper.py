from .domain import domainWrapper
from collections.abc import Callable

from .testDomain import testDomain


domain_name_list =[
    "testDomain"
]





def getDomainNameList()->[str]:
    return domain_name_list


def getConstructor(domainName)->Callable[...,domain]:
    return