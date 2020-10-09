#!/usr/bin/env python3

from flask import Flask, request, jsonify, send_from_directory
from tables import SupportItemTable
import os
import json


class CustomerSupport(object):
    def __init__(self):
        self.supportRequests = []
        self.loginName = None

    def populateDebugSupportRequests(self):
        req = {"input": {"timestamp": 1, "message": "My internet is leaking",
                         "user_name": "Bob the builder", "contact_details": "bob@builder.com"},
               "output": {"timestamp": 2, "sentiment": "angry", "assignee": "John Travolta", "answers": ["Internets don't leak"]}}
        self.supportRequests.append(req)

    def hello_world(self):
        return "Hello World!\nYou might want to navigate to the <a href='web/index.html'>Customer Support Site</a>"

    def webServeFromDirectory(self, path):
        return send_from_directory('web_interface', path)

    def customerRequestCallback(self):
        # TODO(lars)
        print("called customerRequestCallback()")
        # Access elements with something like print(request.form['param2'])
        print(request.form)
        # TODO(lars) call analyzeRequest
        return 'Received the request!\n'  # response to your request.

    def analyzeRequest(self, requestJson):
        pass
        # TODO(jonathan,chris); call assingRequest afterwards

    def assignRequest(self, requestJson):
        pass
        # TODO(jan)

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

    print("Flask server started. Terminate with ctrl+c")
    flaskApp.run(debug=True)  # blocking
