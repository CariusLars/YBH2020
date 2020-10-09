#!/usr/bin/env python3

from flask import Flask, request, jsonify, send_from_directory
from tables import SupportItemTableView, SupportItemTableEdit
import os
import json
import datetime
import ParseMails
import pandas as pd


class CustomerSupport(object):
    def __init__(self):
        self.supportRequests = []
        self.processedRequests = []
        self.loginName = None

        # Read employee table
        raw = pd.read_excel('./../data/mitarbeiterplan.xls')
        self.employees = {x: {} for x in raw}
        for key in self.employees.keys():
            self.employees[key] = {x: 0 for x in raw[key] if str(x) != 'nan'}
        # print(self.employees)

    def populateDebugSupportRequests(self):
        req = {"input": {"timestamp": 1, "message": "My internet is leaking",
                         "user_name": "Bob the builder", "contact_details": "bob@builder.com", 'id': None},
               "output": {"timestamp": 2, "extreme_negative": False, "category": "Glasfaser", "category_score": 14, "assignee": "John Travolta", "answers": ["Internets don't leak"]}}

    def sendAllMailRequests(self):
        list_of_mails = ParseMails.as_json(unique_content=True)
        for mail in list_of_mails:
            self.supportRequests.append(mail)

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

    def assignRequest(self, requestID):
        thresholdUncertainCategory = 4
        #categories_requests = ["Glasfaser", "Kehricht", "Strom", "Internet", "Netz", "Warme", "Mobilitat", "Umzug", "Diverses", "Storungen", "Wasser"]
        #categories_employees = ["Glasfaser", "Kehricht", "Strom", "Internet", "Netz", "Warme", "Mobilitat", "Umzug", "Storungen", "Wasser"]
        request = [request for request in self.processedRequests if request["input"]
                   ["id"] == contactDetailsString][0]

        # Check if this is a diverse request
        if request["output"]["category_score"] <= thresholdUncertainCategory or request["output"]["category"] == "Diverses":
            # Get employee with least emails to process
            all_employees = {}
            for key in self.employees:
                all_employees.update(self.employees[key])
            availableEmployee = min(all_employees, key=all_employees.get)
            # Assign to this employee
            request['output']['assignee'] = availableEmployee
            # Increase counter

        else:
            # Get employee with least emails to process from this category
            availableEmployee = min(
                self.employees[request["output"]["category"]], key=self.employees[request["output"]["category"]].get)
            # Assign to this employee
            request['output']['assignee'] = availableEmployee
            # Increase counter
            self.employees[request["output"]["category"]
                           ][availableEmployee] = self.employees[request["output"]["category"]][availableEmployee] + 1

    def populateDebugProcessedRequests(self):
        response = {"timestamp_request": datetime.datetime.now().strftime("%d.%m.%Y, %H:%M"), "timestamp_reply": -1, "contact_details": "266433173",
                    "user_name": "Lars", "assignee": "Halbes Hähnchen", "message": "Nicht so schlimm, wir liefern schnell eine Neue!"}
        self.processedRequests.append(response)

    def checkProcessedRequestsCallback(self):
        print("called checkProcessedRequestsCallback")
        id = request.args.get('request_id')

        returnElements = [
            processedRequest for processedRequest in self.processedRequests if processedRequest['id'] == id]
        print(self.processedRequests)
        print(returnElements)

        if len(returnElements) > 0:
            return returnElements[-1]
        else:
            return {}

    def generateHtmlTableAllRequestsView(self):
        html_doc = ""
        html_doc += '<form action="generateHtmlTableAllRequestsView" method="get"><input type="submit" value="Refresh"> </form>'
        html_doc += '<form action="loadEmailRequests" method="get"><input type="submit" value="Load Email Requests"> </form>'
        table = SupportItemTableView(self.supportRequests)
        html_doc += table.__html__()
        return html_doc

    def deleteRequestCallback(self):
        html_doc = "Deleted service request from " + request.args.get('id')
        html_doc += '<form action="serviceWorkerProcessing" method="get"><input type="submit" value="Return"> </form>'
        self.supportRequests = [
            item for item in self.supportRequests if item["input"]["user_name"] != request.args.get('id')]
        return html_doc

    def replyRequestCallback(self):
        msg = "Replying to service request from "
        msg += request.args.get('id')
        return msg
        # TODO(jan) make reply mask with reply button

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
            table = SupportItemTableEdit(filteredSupportRequests)
            html_doc += table.__html__()

        return html_doc

    def loginCallback(self):
        self.loginName = request.args.get('name')
        html_doc = "Successfully logged in as " + self.loginName
        html_doc += '<form action="serviceWorkerProcessing" method="get"><input type="submit" value="Let\'s get to work!"> </form>'
        return html_doc

    def logoutCallback(self):
        self.loginName = None
        html_doc = "Successfully logged out"
        html_doc += '<form action="serviceWorkerProcessing" method="get"><input type="submit" value="Goodbye!"> </form>'
        return html_doc


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
    flaskApp.add_url_rule('/web/generateHtmlTableAllRequestsView',
                          view_func=customerSupport.generateHtmlTableAllRequestsView)
    flaskApp.add_url_rule('/web/loadEmailRequests',
                          view_func=customerSupport.sendAllMailRequests)
    flaskApp.add_url_rule(
        '/web/delete', methods=['POST'], view_func=customerSupport.deleteRequestCallback)
    flaskApp.add_url_rule(
        '/web/reply', methods=['POST'], view_func=customerSupport.replyRequestCallback)
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
