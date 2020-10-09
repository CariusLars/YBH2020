#!/usr/bin/env python3

from flask import Flask, request, jsonify, send_from_directory
from tables import SupportItemTable
import os
import json
import datetime
import pandas as pd


class CustomerSupport(object):
    def __init__(self):
        self.supportRequests = []
        self.processedRequests = []
        self.loginName = None

        # Read employee table
        raw = pd.read_excel('./../data/mitarbeiterplan.xls')
        self.employees = {x: {} for x in raw}
        for key in self.employees.keys(): self.employees[key] = {x: 0 for x in raw[key] if str(x) != 'nan'}
        print(self.employees)

    def populateDebugSupportRequests(self):
        req = {"input": {"timestamp": 1, "message": "My internet is leaking",
                         "user_name": "Bob the builder", "contact_details": "bob@builder.com"},
               "output": {"timestamp": 2, "extreme_negative": False, "category":"Glasfaser", "category_score": 14, "assignee": "John Travolta", "answers": ["Internets don't leak"]}}
        self.supportRequests.append(req)

    def hello_world(self):
        return "Hello World!\nYou might want to navigate to the <a href='web/index.html'>Customer Support Site</a>"

    def webServeFromDirectory(self, path):
        return send_from_directory('web_interface', path)

    def customerRequestCallback(self):
        # TODO(lars)
        #print("called customerRequestCallback()")
        # Access elements with something like print(request.form['param2'])
        serviceRequest = {"input": request.form.to_dict(),
                          "output": {"timestamp": -1, "extreme_negative": False, "category": None, "category_score": 0, "assignee": "", "answers": []}}

        self.supportRequests.append(serviceRequest)
        # analyzeRequest(serviceRequest)
        return 'Received the request!\n'  # response to your request.

    def analyzeRequest(self, requestJson):
        pass
        # TODO(jonathan,chris); call assingRequest afterwards

    def assignRequest(self, contactDetailsString):
        thresholdUncertainCategory = 10
        #categories_requests = ["Glasfaser", "Kehricht", "Strom", "Internet", "Netz", "Warme", "Mobilitat", "Umzug", "Diverses", "Storungen", "Wasser"]
        #categories_employees = ["Glasfaser", "Kehricht", "Strom", "Internet", "Netz", "Warme", "Mobilitat", "Umzug", "Bechwerden", "Storungen", "Wasser"]
        request = [request for request in self.processedRequests if request["input"]["contact_details"] == contactDetailsString][0]
        # Check if this is a diverse request
        if request["output"]["category_score"] <= thresholdUncertainCategory or request["output"]["category"] == "Diverses":
            # Get employee with least emails to process

            # Assign to this employee

            # Increase counter
        else:
            # Get employee with least emails to process from this category
            min(self.employees[request["output"]["category"]], key=self.employees[request["output"]["category"]].get)

    def populateDebugProcessedRequests(self):
        response = {"timestamp_request": datetime.datetime.now().strftime("%d.%m.%Y, %H:%M"), "timestamp_reply": -1, "contact_details": "266433173",
                    "user_name": "Lars", "assignee": "Halbes Hähnchen", "message": "Nicht so schlimm, wir liefern schnell eine Neue!"}
        self.processedRequests.append(response)

    def checkProcessedRequestsCallback(self):
        print("called checkProcessedRequestsCallback")
        user_id = request.args.get('request_id')

        returnElements = [
            processedRequest for processedRequest in self.processedRequests if processedRequest['contact_details'] == user_id]
        print(self.processedRequests)
        print(returnElements)

        if len(returnElements) > 0:
            return returnElements[-1]
        else:
            return {}

    def generateHtmlTableAllRequests(self):
        table = SupportItemTable(self.supportRequests)
        return table.__html__()

    def deleteRequestCallback(self):
        msg = "Deleted service request from "
        msg += request.args.get('id')
        return msg

    def serviceWorkerProcessing(self):
        html_doc = ""

        if self.loginName is None:
            html_doc += "<p>Please log in</p>"
            html_doc += '<form action="login" method="get"> Name: <input type="text" name="name"> <input type="submit" value="Submit"> </form>'
        else:
            html_doc += "<p>Logged in as " + self.loginName + "</p>"
            html_doc += '<form action="logout" method="get"><input type="submit" value="Logout"> </form>'
            html_doc += 'The following tickets have been assigned to you:<br>'
            filteredSupportRequests = [
                supportRequest for supportRequest in self.supportRequests if supportRequest["output"]["assignee"] == self.loginName]
            table = SupportItemTable(filteredSupportRequests)
            html_doc += table.__html__()

        return html_doc

    def loginCallback(self):
        self.loginName = request.args.get('name')
        return "Successfully logged in as " + self.loginName

    def logoutCallback(self):
        self.loginName = None
        return "Successfully logged out"


if __name__ == "__main__":
    customerSupport = CustomerSupport()
    static_file_dir = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'static')
    flaskApp = Flask(__name__, static_url_path=static_file_dir)

    # declare flask callbacks
    flaskApp.add_url_rule('/', view_func=customerSupport.hello_world)
    flaskApp.add_url_rule('/customerRequestCallback',
                          methods=['POST'], view_func=customerSupport.customerRequestCallback)
    flaskApp.add_url_rule('/checkProcessedRequestsCallback',
                          methods=['GET'], view_func=customerSupport.checkProcessedRequestsCallback)
    flaskApp.add_url_rule('/customerSupport',
                          view_func=customerSupport.hello_world)
    flaskApp.add_url_rule('/web/<path:path>',
                          view_func=customerSupport.webServeFromDirectory)
    flaskApp.add_url_rule('/web/generateHtmlTableAllRequests',
                          view_func=customerSupport.generateHtmlTableAllRequests)
    flaskApp.add_url_rule(
        '/delete', methods=['POST'], view_func=customerSupport.deleteRequestCallback)
    flaskApp.add_url_rule('/web/serviceWorkerProcessing',
                          view_func=customerSupport.serviceWorkerProcessing)
    flaskApp.add_url_rule(
        '/web/login', view_func=customerSupport.loginCallback)
    flaskApp.add_url_rule(
        '/web/logout', view_func=customerSupport.logoutCallback)

    # Debugging, remove later
    customerSupport.populateDebugSupportRequests()
    customerSupport.populateDebugProcessedRequests()

    print("Flask server started. Terminate with ctrl+c")
    flaskApp.run(debug=True)  # blocking
