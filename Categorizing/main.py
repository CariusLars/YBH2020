#!/usr/bin/env python3

from flask import Flask, request, jsonify, send_from_directory
import os


class CustomerSupport(object):
    def __init__(self):
        pass

    # Serving a normal HTTP GET request (e.g., from browser, port 80)
    # @flaskApp.route("/")
    def hello_world(self):
        return "Hello World!\nYou might want to navigate to the <a href='web/index.html'>Customer Support Site</a>"

    # test query with
    # curl --data "param1=value1&param2=value2&foo=123{a:b, c:d}&otherData=blub" 127.0.0.1:5000/process
    # just allows POST requests

    def webServeFromDirectory(self, path):
        print("webServeFromDirectory called with path=", path)
        return send_from_directory('web_interface', path)

    def customerRequestCallback(self):
        # TODO(lars)
        print("called customerRequestCallback()")
        # Access elements with something like print(request.form['param2'])
        # TODO(lars) call analyzeRequest
        return 'Received the request!\n'  # response to your request.

    def analyzeRequest(self, requestJson):
        pass
        # TODO(jonathan,chris); call assingRequest afterwards

    def assignRequest(self, requestJson):
        pass
        # TODO(jan)

    def customerSupportOverview(self):
        pass


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

    print("Flask server started. Terminate with ctrl+c")
    flaskApp.run(debug=True)  # blocking
