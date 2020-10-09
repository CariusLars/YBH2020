#!/usr/bin/env python3

from flask import Flask, request, jsonify


class CustomerSupport(object):
    def __init__(self):
        pass

    # Serving a normal HTTP GET request (e.g., from browser, port 80)
    # @flaskApp.route("/")
    def hello_world(self):
        return "Hello World!"

    # test query with
    # curl --data "param1=value1&param2=value2&foo=123{a:b, c:d}&otherData=blub" 127.0.0.1:5000/process
    # just allows POST requests

    def customerRequestCallback(self):
        print("called customerRequestCallback()")
        # Access elements with something like print(request.form['param2'])
        return 'Received the request!\n'  # response to your request.


if __name__ == "__main__":
    customerSupport = CustomerSupport()
    flaskApp = Flask(__name__)

    # declare flask callbacks
    flaskApp.add_url_rule('/', view_func=customerSupport.hello_world)
    # to test: curl --data "param1=value1&param2=value2&foo=123{a:b, c:d}&otherData=blub" 127.0.0.1:5000/customerRequestCallback
    flaskApp.add_url_rule('/customerRequestCallback',
                          methods=['POST'], view_func=customerSupport.customerRequestCallback)

    print("Flask server started. Terminate with ctrl+c")
    flaskApp.run(debug=True)  # blocking
