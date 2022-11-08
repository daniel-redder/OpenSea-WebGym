import flask
from flask import jsonify, request, send_file, Response
import pickleJar as pj
from domains.domain import domainWrapper
import cv2
import os, sys
import numpy as np

#--------------------------Imports---------------------------------------#
from gym.core import ObsType

from domains import domainHelper

import atexit


#------------------------ atexit thread ---------------------------------#

def on_exit():
    pj.clear_cache()

atexit.register(on_exit)



#------------------------configuration-----------------------------------#


app = flask.Flask(__name__,template_folder="templates")




#-------------------------------- GUI PAGES --------------------------------------------------

#-------------------------------- Debugging Webpages -----------------------------------------
"""
Use this for debugging, this will show api keys to anyone who can access the site so be sure to not use this on a open network. 
"""

@app.route("/")
@app.route("/home")
def index():
    cached_instances = pj.get_cache()
    return flask.render_template("index.html",cached_instances = cached_instances)


  
@app.route("/env/details/<envID>",methods=["POST"])
def details(envID):
    data = pj.get_data(envID)
    return flask.render_template("details.html",data=data)
    
#----------------------------------------------------------------------------------------------
  


#TODO list for REST QUERY system
#----------------------------------------------------- required for functionality ---------------------



#----------------------------------- low priority -------------------------------------------------

#TODO implement other environment attribute fetching as per https://www.gymlibrary.dev/api/core/


#----------------------------------------------------------------------------------------------------

#------------------------------- API CALLS ----------------------------------------------------------------


@app.route("/ping",methods=["POST","GET"])
def ping():
    return {"message":"successful connection"}



@app.route("/env/createzoo/<domainName>",methods=["POST","GET"])
def createEnvironment(domainName):
    """
    Creates a domain environment with the listed params

    :param domainName:
    :return: Json list of api keys and instance id || error
    """

    # if request.method == "POST":
    data = request.get_json()
    #print(data["agentCount"])
    # else:
    #     print("test")
    #     data = {}

    if not  domainName == request.view_args["domainName"]:
        return {"error":"internal domainName param matching error see createDomain, admin"}



    domainList = domainHelper.getDomainNameList()

    if not domainName in domainList:
        return {"error":"domain not found"}

    #try:

    environment=domainHelper.getConstructor(domainName)

    if environment == False:
        return {"error":"error in finding environment"}

    environment = environment(*data)
    environment.reset()
    try:
        print(data["agentCount"])
    except:
        data["agentCount"] = len(environment.agents)

    envID, apiKeys = pj.createInstance(domainName=domainName, agentCount=data["agentCount"], domain = environment)

    return {"agent_api_keys":apiKeys,"env_id":envID}


    # except Exception as e:
    #     print(e)
    #     return {"error":" caught in domain instancing"}



@app.route("/env/checkzoo/<domainName>/<env_id>/<api_key>",methods=["POST","GET"])
def whosTurn(domainName,env_id,api_key):
    result = pj.getInstance(envID=env_id, domainName=domainName,apiKey=api_key)

    if result == False:
        return {"error":"invalid environment lookup, possibly bad apikey"}

    return {"agent":result.currAgent}


@app.route("/env/stepzoo/<domainName>/<env_id>/<api_key>",methods=["POST","GET"])
def stepEnvironment(domainName,env_id,api_key)->(ObsType, float, bool, bool, dict):
    """

    :param domainName: name of the domain
    :param env_id: unique id of domain instance
    :param api_key: unique api_key of agent for instance of domain
    :return: Tuple[ObsType, float, bool, bool, dict]
    :returns: https://www.gymlibrary.dev/api/core/ via json
    """

    result = pj.getInstance(envID=env_id,domainName=domainName,apiKey=api_key)

    if result == False:
        return {"error":"invalid environment lookup, possibly bad apiKey"}

    try:
        action = request.get_json()["action"]
    except:
        return {"error":"no action provided"}

    result.domain.step(action)
    result.domain.stepAEC()

    return {}


@app.route("/env/lastzoo/<domainName>/<env_id>/<api_key>",methods=["POST","GET"])
def lastEnvironment(domainName, env_id, api_key):
    """

    :param domainName:
    :param env_id:
    :param api_key:
    :return:
    """
    result = pj.getInstance(envID=env_id, domainName=domainName, apiKey=api_key)

    if result == False:
        return {"error": "invalid environment lookup, possibly bad apiKey"}

    obs, reward, termination, truncation, info = result.domain.last()

    return {"observation":obs,"reward":reward,"termination":termination,"truncation":truncation, "info":info}


@app.route("/env/resetgym/<domainName>/<env_id>/<api_key>",methods=["POST","GET"])
def resetEnvironment(domainName,env_id,api_key)->(ObsType, dict):
    """

    :param domainName:
    :param env_id:
    :param api_key:
    :return:
    """

    result = pj.getInstance(envID=env_id, domainName=domainName, apiKey=api_key)

    if result == False:
        return {"error": "invalid environment lookup, possibly bad apiKey"}

    result.domain.reset()

    return {}



app.run(port=8080)








