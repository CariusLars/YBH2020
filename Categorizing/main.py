#!/usr/bin/env python3

from flask import Flask, request, jsonify, send_from_directory
from tables import SupportItemTableView, SupportItemTableEdit
import os
import json
import datetime
import ParseMails
import pandas as pd
import nlp
import SimilarityScore


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
        self.links = {"Glasfaser": [("Internet und Glasfaser Produktinfos", "https://www.ewb.ch/privatkunden/angebot/internet")], "Kehricht": [], "Strom": [("Strom Produktinfos", "https://www.ewb.ch/privatkunden/angebot/strom-beziehen"), ("Solaranlage / Strom produzieren Produktinfos", "https://www.ewb.ch/privatkunden/angebot/strom-produzieren"), ("Solarrechner", "https://www.ewb-solarrechner.ch/"), ("Energieberatung und Contracting Produktinfos", "https://www.ewb.ch/privatkunden/angebot/dienstleistungen")], "Internet": [("ewb Internet und TV", "https://www.ewwwb.ch/"), ("Internet und Glasfaser Produktinfos", "https://www.ewb.ch/privatkunden/angebot/internet")], "Netz": [("Netzdienstleistungen Produktinfos", "https://www.ewb.ch/privatkunden/angebot/netz-nutzen")],
                      "Warme": [("Fernwaerme Produktinfos", "https://www.ewb.ch/privatkunden/angebot/fernwaerme"), ("Gas Produktinfos", "https://www.ewb.ch/privatkunden/angebot/waerme-aus-gas")], "Mobilitat": [("Mobilitaet Produktinfos", "https://www.ewb.ch/privatkunden/angebot/mobilitaet"), ("Move Elektromobilitaet", "http://www.move.ch/")], "Umzug": [("Umzugsmeldung", "https://www.ewb.ch/kundenservice/kundendienst-kontakt/anmeldung-umzug")], "Diverses": [("uebersicht FAQ und weiteres Wissen", "https://www.ewb.ch/wissen"), ("uebersicht Baustellen", "https://map.bern.ch/stadtplan/?grundplan=stadtplan_farbig&koor=2600650,1199750&zoom=2&hl=0&layer="), ("Energieberatung und Contracting Produktinfos", "https://www.ewb.ch/privatkunden/angebot/dienstleistungen")],
                      "Storungen": [("Meldung defekte/ storende Beleuchtung"), ("https://www.ewb.ch/kundenservice/kundendienst-kontakt/meldeformular-defekte-leuchten/detail")], "Wasser": [("Wassertarife Stadt Bern", "https://stadtrecht.bern.ch/lexoverview-home/lex-752_312"), ("Abwassertarife Stadt Bern", "https://stadtrecht.bern.ch/lexoverview-home/lex-821_12"), ("Wasserhaerte in der Stadt Bern", "https://www.ewb.ch/wissen/wissen/wissen-wasser-wasserhaerte")]}

    def populateDebugSupportRequests(self):
        req = {"input": {"timestamp": 1, "message": "My internet is leaking",
                         "user_name": "Bob the builder", "contact_details": "bob@builder.com", 'id': 7},
               "output": {"timestamp": 2, "extreme_negative": False, "category": "Glasfaser", "category_score": 14, "assignee": "John Travolta", "answers": ["Internets don't leak"]}}
        self.supportRequests.append(req)

    def sendAllMailRequests(self):
        list_of_mails = ParseMails.as_json(unique_content=True, shortest=10)
        for mail in list_of_mails:
            self.supportRequests.append(mail)
            self.analyzeRequest(mail['input']['id'])
        return 'Emails erfolgreich importiert<form action="generateHtmlTableAllRequestsView" method="get"><input type="submit" value="Zurueck zur Ubersicht"> </form>'

    def hello_world(self):
        return "Hello World!\nYou might want to navigate to the <a href='web/index.html'>Customer Support Site</a>"

    def webServeFromDirectory(self, path):
        return send_from_directory('web_interface', path)

    def customerRequestCallback(self):
        # TODO(lars)
        print("called customerRequestCallback()")
        # Access elements with something like print(request.form['param2'])
        serviceRequest = {"input": request.form.to_dict(),
                          "output": {"timestamp": -1, "extreme_negative": False, "category": None, "category_score": 0, "assignee": "", "answers": []}}

        self.supportRequests.append(serviceRequest)

        self.analyzeRequest(serviceRequest["input"]["id"])
        return 'Received the request!\n'  # response to your request.

    def analyzeRequest(self, requestID):
        # print(self.supportRequests)
        request = [
            request for request in self.supportRequests if request["input"]["id"] == requestID][0]
        resultDict = nlp.packaged_results(request["input"]["id"], request["input"]["timestamp"],
                                          request["input"]["message"], request["input"]["user_name"], request["input"]["contact_details"])
        request["output"]["category"] = resultDict["category"]
        request["output"]["category_score"] = resultDict["category_score"]
        request["output"]["extreme_negative"] = resultDict["extreme_negative"]

        # Calculate most probable FAQs
        if resultDict["category_score"] > 4:
            category_only = resultDict["category"]
        else:
            category_only = None
        request["output"]["answers"] = SimilarityScore.calculate(
            request["input"]["message"], 3, category_only)

        self.assignRequest(requestID)
        # print(self.supportRequests)
        # print(request)
        # print(resultDict)
        # TODO(jonathan,chris); call assingRequest afterwards

    def assignRequest(self, requestID):
        thresholdUncertainCategory = 4
        #categories_requests = ["Glasfaser", "Kehricht", "Strom", "Internet", "Netz", "Warme", "Mobilitat", "Umzug", "Diverses", "Storungen", "Wasser"]
        #categories_employees = ["Glasfaser", "Kehricht", "Strom", "Internet", "Netz", "Warme", "Mobilitat", "Umzug", "Storungen", "Wasser"]
        request = [request for request in self.supportRequests if request["input"]
                   ["id"] == requestID][0]

        # Check if this is a diverse request
        if request["output"]["category_score"] <= thresholdUncertainCategory or request["output"]["category"] == "Diverses":
            print("Diverse request. Category {}, Score {}".format(
                request["output"]["category"], request["output"]["category_score"]))
            # Get employee with least emails to process
            all_employees = {}
            for key in self.employees:
                all_employees.update(self.employees[key])
            availableEmployee = min(all_employees, key=all_employees.get)
            # Assign to this employee
            request['output']['assignee'] = availableEmployee
            # Increase counter
            for key in self.employees:
                if availableEmployee in self.employees[key].keys():
                    self.employees[key][availableEmployee] = self.employees[key][availableEmployee] + 1
                    break

        else:
            # Get employee with least emails to process from this category
            availableEmployee = min(
                self.employees[request["output"]["category"]], key=self.employees[request["output"]["category"]].get)
            # Assign to this employee
            request['output']['assignee'] = availableEmployee
            # Increase counter
            self.employees[request["output"]["category"]
                           ][availableEmployee] = self.employees[request["output"]["category"]][availableEmployee] + 1
        # print("supportRequests:")
        # print(self.supportRequests)
        #print("Employee Status")
        # print(self.employees)

    def populateDebugProcessedRequests(self):
        response = {"id": 1234, "timestamp_request": datetime.datetime.now().strftime("%d.%m.%Y, %H:%M"), "timestamp_reply": -1, "contact_details": "266433173",
                    "user_name": "Lars", "assignee": "Halbes Haehnchen", "message": "Nicht so schlimm, wir liefern schnell eine Neue!"}
        self.processedRequests.append(response)

    def checkProcessedRequestsCallback(self):
        print("called checkProcessedRequestsCallback")
        id = request.args.get('request_id')

        returnElements = [
            processedRequest for processedRequest in self.processedRequests if processedRequest['id'] == id]
        # print(self.processedRequests)
        # print(returnElements)

        if len(returnElements) > 0:
            return returnElements[-1]
        else:
            return {}

    def generateHtmlTableAllRequestsView(self):
        html_doc = ""
        html_doc += '<form action="generateHtmlTableAllRequestsView" method="get"><input type="submit" value="Aktualisieren"> </form>'
        html_doc += '<form action="loadEmailRequests" method="get"><input type="submit" value="Email Anfragen Importieren"> </form>'
        filteredSupportRequests = [
            supportRequest for supportRequest in self.supportRequests if supportRequest["output"]["assignee"] != "done"]
        table = SupportItemTableView(filteredSupportRequests)
        html_doc += table.__html__()
        return html_doc

    def deleteRequestCallback(self):
        html_doc = "Deleted service request from " + request.args.get('id')
        html_doc += '<form action="serviceWorkerProcessing" method="get"><input type="submit" value="Return"> </form>'
        self.supportRequests = [
            item for item in self.supportRequests if item["input"]["user_name"] != request.args.get('id')]
        return html_doc

    def replyRequestCallback(self):
        print(request.args.get('id'))
        print(self.supportRequests)
        print([
            currentRequest for currentRequest in self.supportRequests if
            currentRequest["input"]["id"] == request.args.get('id')])
        currentRequest = [
            currentRequest for currentRequest in self.supportRequests if
            currentRequest["input"]["id"] == request.args.get('id')][0]

        html_doc = "<p>Anfrage von Nutzer: "
        html_doc += "<b>" + \
            currentRequest["input"]["user_name"] + "</b><br></p>"
        html_doc += "<p><b>Service-Anfrage: </b><br></p>"
        html_doc += "<i>" + currentRequest["input"]["message"] + "</i>"
        html_doc += "<p><br> Aehnliche Fragen & Antworten: <br></p>"
        for pair in currentRequest["output"]["answers"]:
            html_doc += "<b>" + pair[0] + "?</b>"
            html_doc += "<br>"
            html_doc += pair[1]
            html_doc += "<br><br>"

        html_doc += "<p><b>Nuetzliche Links: </b><br></p>"
        for (description, link) in self.links[currentRequest["output"]["category"]]:
            html_doc += description + ": " + "<a href=\"" + link + "\">" + link + "</a><br>"
        if currentRequest["output"]["category_score"] <= 4:
            for (description, link) in self.links["Diverses"]:
                html_doc += description + ": " + "<a href=\"" + link + "\">" + link + "</a><br>"

        html_doc += "<p><br>Antwort eingeben:</p>"
        html_doc += '<form action="send_reply" method="get"> <textarea name="message" cols="100" rows="10"></textarea> ID: <input type="text" value="{}" name="id" readonly> <input type="submit" value="Senden"> </form>'.format(
            request.args.get('id'))
        return html_doc

    def sendReplyRequestCallback(self):
        html_doc = "<p> You've replied successfully</p>"
        html_doc += '<form action="serviceWorkerProcessing" method="get"><input type="submit" value="Back to ticket overview"> </form>'
        # Send reply to Telegram bot
        try:
            currentRequest = [
                currentRequest for currentRequest in self.supportRequests if currentRequest["input"]["id"] == request.args.get('id')][0]
            response = {"id": request.args.get('id'), "timestamp_request": currentRequest["input"]["timestamp"],
                        "timestamp_reply": datetime.datetime.now().strftime("%d.%m.%Y, %H:%M"), "contact_details": currentRequest["input"]["contact_details"],
                        "user_name": currentRequest["input"]["user_name"], "assignee": currentRequest["output"]["assignee"],
                        "message": request.args.get('message')}
            self.processedRequests.append(response)

            # Reduce count of pending emails for assignee
            all_employees = {}
            for key in self.employees:
                all_employees.update(self.employees[key])
            for key in self.employees:
                if currentRequest["output"]["assignee"] in self.employees[key].keys():
                    self.employees[key][currentRequest["output"]["assignee"]
                                        ] = self.employees[key][currentRequest["output"]["assignee"]] - 1
                    break
            # Update database
            currentRequest["output"]["assignee"] = "done"
        except:
            pass

        return html_doc

    def serviceWorkerProcessing(self):
        html_doc = ""

        if self.loginName is None:
            html_doc += "<p>Bitte melden Sie sich an</p>"
            html_doc += '<form action="login" method="get"> Name: <input type="text" name="name"> <input type="submit" value="Login"> </form>'
        else:
            html_doc += "<p>Angemeldet als: " + self.loginName + "</p>"
            html_doc += '<form action="logout" method="get"><input type="submit" value="Logout"> </form>'
            html_doc += 'Ihnen wurden die folgenden Anfragen zugeteilt:<br>'
            filteredSupportRequests = [
                supportRequest for supportRequest in self.supportRequests if supportRequest["output"]["assignee"] == self.loginName]
            table = SupportItemTableEdit(filteredSupportRequests)
            html_doc += table.__html__()

        return html_doc

    def loginCallback(self):
        self.loginName = request.args.get('name')
        html_doc = "Erfolgreich angemeldet als " + self.loginName
        html_doc += '<form action="serviceWorkerProcessing" method="get"><input type="submit" value="Service-Anfragen bearbeiten"> </form>'
        return html_doc

    def logoutCallback(self):
        self.loginName = None
        html_doc = "Abmeldung erfolgreich"
        html_doc += '<form action="serviceWorkerProcessing" method="get"><input type="submit" value="Auf Wiedersehen!"> </form>'
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
    flaskApp.add_url_rule(
        '/web/reply', view_func=customerSupport.replyRequestCallback)
    flaskApp.add_url_rule(
        '/web/send_reply', view_func=customerSupport.sendReplyRequestCallback)

    @flaskApp.errorhandler(404)
    def page_not_found(e):
        return "page not found", 404

    # Debugging, remove later
    # customerSupport.populateDebugSupportRequests()
    # customerSupport.populateDebugProcessedRequests()

    print("Flask server started. Terminate with ctrl+c")
    flaskApp.run(host='0.0.0.0', debug=False)  # blocking
