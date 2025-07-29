import time
import uuid
import numpy as np
from  datetime import datetime
from dateutil import parser
import requests
import json
import base64
import os
from dotenv import load_dotenv
load_dotenv()

subscriptionUrl = os.getenv("SUBSCRIPTION_URL")
getStreamdataUrl = os.getenv("DATA_STREAM_URL")



def getProcessID():
    return f"{int(time.time() * 1000)}{uuid.uuid4()}"


def getInputPopulatedPrompt(promptTemplate, tempObj):
    for key, value in tempObj.items():
        promptTemplate = promptTemplate.replace(f"{{{{{key}}}}}", value)
    return promptTemplate

def costColumnMapping(costResults, allProcess):
    # this dict will store cost column data for each row
    cost_cols = {}

    compressed_prompt = []
    compressed_prompt_output = []
    cost = []
    cost_saving = []

    for record in allProcess:
        cost_cols[record] = []
        for item in costResults:
            if list(item.keys())[0].split("-")[0] == record.split("-")[0]:
                cost_cols[record].append(list(item.values())[0])

    for ky, val in cost_cols.items():
        try:
            compressed_prompt.append(val[0])
        except IndexError:
            compressed_prompt.append("error occured")

        try:
            compressed_prompt_output.append(val[1])
        except IndexError:
            compressed_prompt_output.append("error occured")

        try:
            cost.append(val[2])
        except IndexError:
            cost.append("error occured")

        try:
            cost_saving.append(val[3])
        except IndexError:
            cost_saving.append("error occured")

    return compressed_prompt, compressed_prompt_output, cost, cost_saving


def checkUserHits(workspaceID, hasSubscribed, trialEndDate, subscriptionEndDate, remainingHits, datasetLength):
    # Get the current date (only the date part)
    current_date = datetime.now().date()

    # Parse trialEndDate if provided
    if trialEndDate is not None:
        try:
            trialEndDate = parser.parse(trialEndDate).date()
        except Exception:
            return {"success": False, "message": "Invalid trialEndDate format"}

    # Parse subscriptionEndDate if provided
    if subscriptionEndDate is not None:
        try:
            subscriptionEndDate = parser.parse(subscriptionEndDate).date()
        except Exception:
            return {"success": False, "message": "Invalid subscriptionEndDate format"}

    # If user is on a free trial
    if not hasSubscribed and trialEndDate is not None:
        if current_date > trialEndDate:
            return {"success": False, "message": "Trial expired. Access denied"}

        if remainingHits < datasetLength or remainingHits <= 0:
            return {"success": False, "message": "Trial Hits Exhausted"}

    else:
        if subscriptionEndDate and current_date > subscriptionEndDate:
            return {"success": False, "message": "Subscription expired. Access denied."}

        if remainingHits <= 0 or remainingHits < datasetLength:
            headers = {
                "Authorization": f"Bearer {base64.b64encode(workspaceID.encode()).decode()}",
                "Content-Type": "application/json",
            }
            reqBody = {"unitsToSet": 1}
            responseBody = requests.post(url=subscriptionUrl, json=reqBody, headers=headers)
            response = json.loads(responseBody.text)

            proceed = response.get("execution", "")
            print(proceed)

            if proceed:
                return {"success": True, "message": "Hits added and access granted."}

    return {"success": True, "message": "Access granted."}

def getStreamId(workspaceID: str, token, dataStreamName):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    reqBody = {"workspaceID": workspaceID}
    response = requests.post(url=getStreamdataUrl, json=reqBody, headers=headers)

    if response.status_code == 200:
        responseJson = response.json()
        data = responseJson.get("data", [])

        # Find stream by name
        matchedStream = next((stream for stream in data if stream.get("name") == dataStreamName), None)

        if matchedStream:
            
            return matchedStream.get("dataStreamID")
            
        else:
            print(f"No stream found with name: {dataStreamName}")
            return None
    else:
        print("Error:", response.status_code, response.text)
        return None