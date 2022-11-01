import flask
from flask import jsonify, request, send_file, Response
import sqltool
from domains.domain import domainWrapper
import cv2
import os, sys
import numpy as np

#--------------------------Imports---------------------------------------#
from gym.core import ObsType

from domains import domainHelper


#------------------------configuration-----------------------------------#


app = flask.Flask(__name__,template_folder="templates")




#-------------------------------- GUI PAGES --------------------------------------------------

@app.route("/")
@app.route("/home")
def index():
    return flask.render_template("index.html")

@app.route("/env/details/<envID>",methods=["POST"])
def



#TODO list for REST QUERY system
#----------------------------------------------------- required for functionality ---------------------

#TODO update json errors with proper error returns
#TODO save environment state
#TODO implement this later - steps
#TODO implement this later - reset



#----------------------------------- low priority -------------------------------------------------

#TODO implement other environment attribute fetching as per https://www.gymlibrary.dev/api/core/


#----------------------------------------------------------------------------------------------------

#------------------------------- API CALLS ----------------------------------------------------------------

@app.route("/env/createzoo/<domainName>",methods=["POST"])
def createEnvironment(domainName):
    """
    Creates a domain environment with the listed params

    :param domainName:
    :return: Json list of api keys and instance id || error
    """

    if request.method == "POST":
        data = request.get_json()

    else:
        return {"error":"post request not provided for create Domain"}

    if not  domainName == request.view_args["domainName"]:
        return {"error":"internal domainName param matching error see createDomain, admin"}

    try:
        print(request.view_args["agentCount"])
    except:
        return {"error":"remember to include agentCount"}

    domainList = domainHelper.getDomainNameList()

    if not domainName in domainList:
        return {"error":"domain not found"}

    try:

        environment=domainHelper.getConstructor(domainName)(*data)
        envID, apiKeys = sqltool.createInstance(domainName=domainName, agentCount=request.view_args["agentCount"], domain = environment)

        return {"agent_api_keys":apiKeys,"env_id":envID}


    except Exception as e:
        return {"error":e+" caught in domain instancing"}





@app.route("/env/stepzoo/<domainName>/<env_id>/<api_key>",methods=["POST"])
def stepEnvironment(domainName,env_id,api_key)->tuple[ObsType, float, bool, bool, dict]:
    """

    :param domainName: name of the domain
    :param env_id: unique id of domain instance
    :param api_key: unique api_key of agent for instance of domain
    :return: Tuple[ObsType, float, bool, bool, dict]
    :returns: https://www.gymlibrary.dev/api/core/ via json
    """

    #TODO implement this later - steps

    pass



@app.route("/env/resetgym/<domainName>/<env_id>/<api_key>")
def resetEnvironment(domainName,env_id,api_key)->tuple[ObsType, dict]:
    """

    :param domainName:
    :param env_id:
    :param api_key:
    :return:
    """



    pass











