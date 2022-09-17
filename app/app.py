import flask
from flask import jsonify, request, send_file, Response
import cv2
import os, sys
import numpy as np

#-----------------------------------------------------------------#
from domains import domainHelper


#------------------------imports-----------------------------------#


app = flask.Flask(__name__,template_folder="templates")

@app.route("/")
@app.route("/home")
def index():
    return flask.render_template("index.html")



#TODO list for REST QUERY system
#TODO update json errors with proper error returns



@app.route("/env/create/<domainName>",methods=["POST"])
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


    domainList = domainHelper.getDomainNameList()

    if not domainName in domainList:
        return {"error":"domain not found"}

    try:

        environment=domainHelper.getConstructor(domainName)(*data)
        return {"agent_api_keys":environment.get_agent_api(),"env_id":environment.id}

    except Exception as e:
        return {"error":e+" caught in domain instancing"}
