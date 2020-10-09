#!/usr/bin/env python3

from flask import Flask, request, jsonify, send_from_directory
from tables import SupportItemTable
import os
import json


class CustomerSupport(object):
    def __init__(self):
        self.supportRequests = []

    def populateDebugSupportRequests(self):
        req = {"input": {"timestamp": 1, "message": "My internet is leaking",
                         "user_name": "Bob the builder", "contact_details": "bob@builder.com"},
               "output": {"timestamp": 2, "sentiment": "angry", "assignee": "John Travolta", "answers": ["Internets don't leak"]}}
        self.supportRequests.append(req)

    def hello_world(self):
        return "Hello World!\nYou might want to navigate to the <a href='web/index.html'>Customer Support Site</a>"

    def webServeFromDirectory(self, path):
        print("webServeFromDirectory called with path=", path)
        return send_from_directory('web_interface', path)

    def customerRequestCallback(self):
        # TODO(lars)
        #print("called customerRequestCallback()")
        # Access elements with something like print(request.form['param2'])
        serviceRequest = {"input": request.form.to_dict(),
               "output": {"timestamp": -1, "sentiment": [], "sentiment_prob": [], "categories": [], "categories_prob": [], "assignee": "", "answers": []}}

        self.supportRequests.append(serviceRequest)
        #analyzeRequest(serviceRequest)
        return 'Received the request!\n'  # response to your request.

    def analyzeRequest(self, requestJson):
        pass
        # TODO(jonathan,chris); call assingRequest afterwards

    def assignRequest(self, requestJson):
        pass
        # TODO(jan)

    def respondToCustomer(self, respondJson):
        pass

    def generateHtmlTableAllRequests(self):
        items = [dict(name='Name1', topic='Topic1'),
                 dict(name='Name2', topic='Topic2'),
                 dict(name='Name3', topic='Topic3')]
        table = SupportItemTable(items)
        return table.__html__()


if __name__ == "__main__":
    customerSupport = CustomerSupport()
    static_file_dir = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'static')
    flaskApp = Flask(__name__, static_url_path=static_file_dir)

    # declare flask callbacks
    flaskApp.add_url_rule('/', view_func=customerSupport.hello_world)
    # to test: curl --data "param1=value1&param2=value2&foo=123{a:b, c:d}&otherData=blub" 127.0.0.1:5000/customerRequestCallback
    flaskApp.add_url_rule('/customerRequestCallback',
                          methods=['POST'], view_func=customerSupport.customerRequestCallback)
    flaskApp.add_url_rule('/customerSupport',
                          view_func=customerSupport.hello_world)
    flaskApp.add_url_rule('/web/<path:path>',
                          view_func=customerSupport.webServeFromDirectory)
    flaskApp.add_url_rule('/web/generateHtmlTableAllRequests',
                          view_func=customerSupport.generateHtmlTableAllRequests)

    # Debugging, remove later
    customerSupport.populateDebugSupportRequests()

    print("Flask server started. Terminate with ctrl+c")
    flaskApp.run(debug=True)  # blocking
