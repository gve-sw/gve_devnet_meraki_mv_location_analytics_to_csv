"""
Copyright (c) 2023 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

# code pulls cmx data from Meraki access point and saves in cmxData.csv file
# Libraries
from pprint import pprint
import os
from flask import Flask
from flask import json
from flask import request
import sys, getopt
from datetime import datetime
import csv
import shutil
import json, requests, os, time
from config import ORG_IDS, MERAKI_API_KEY, validators, secrets, version
from pytz import timezone
from config import initialRSSIThreshold, visitorRSSIThreshold, maxSecondsAwayNewVisit, minMinutesVisit, theTimeZone, summaryTimePeriod

csvinputfile = None
csvoutputfile = None

############## USER DEFINED SETTINGS ###############
# MERAKI SETTINGS
csvfile = None
header_written = False
valid_requester_ips = ['<ip 1>', '<ip 2>'] #Use if dealing with multiple orgs
devicesMapper={}
apNames={}

def setTimeTrackers():
    global dayTracker, hourTracker, monthTracker, testTracker, yearTracker
    tz = timezone(theTimeZone)
    theLocalTime = datetime.now(tz)
    yearTracker=theLocalTime.year
    monthTracker=theLocalTime.month
    dayTracker=theLocalTime.day
    hourTracker=theLocalTime.hour
    testTracker=int(theLocalTime.minute/10)

# gets meraki devices
def getDevices(network):
    # Get video link
    url = "https://api.meraki.com/api/v0/networks/"+network+"/devices/"

    headers = {
        'X-Cisco-Meraki-API-Key': MERAKI_API_KEY,
        "Content-Type": "application/json"""
    }
    resp = requests.request("GET", url, headers=headers)
    # print(resp)
    if int(resp.status_code / 100) == 2:
        return(resp.text)
    return('link error')

def getNetworks(org):
    url = "https://api.meraki.com/api/v0/organizations/" + org + "/networks/"
    headers = {
        'X-Cisco-Meraki-API-Key': MERAKI_API_KEY,
        "Content-Type": "application/json"""
    }
    resp = requests.request("GET", url, headers=headers)
    # print(resp)
    # if int(resp.status_code / 100) == 2:
    if int(resp.status_code) == 200:
        return (resp.text)
    return ('link error')

def save_to_csv(data):
    # Ensure the 'reports' directory exists
    if not os.path.exists('reports'):
        os.makedirs('reports')

    # Create a serialized filename based on the current timestamp
    filename = 'reports/cmxData_{}.csv'.format(datetime.now().strftime('%Y%m%d_%H%M%S'))

    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['manufacturer', 'mac', 'lat', 'lng', 'rssi', 'seenTime']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Check if the file is empty to write the header
        if csvfile.tell() == 0:
            writer.writeheader()

        for observation in data['observations']:
            lat = observation['location']['lat'] if 'location' in observation and observation['location'] else None
            lng = observation['location']['lng'] if 'location' in observation and observation['location'] else None
            writer.writerow({
                'manufacturer': observation.get('manufacturer', ''),
                'mac': observation.get('clientMac', ''),
                'lat': lat,
                'lng': lng,
                'rssi': observation.get('rssi', ''),
                'seenTime': observation.get('seenTime', '')
            })

# Save CMX Data for Recepcion
def save_data(data):
    # Ensure the 'reports' directory exists
    if not os.path.exists('reports'):
        os.makedirs('reports')

    # Create a serialized filename based on the current timestamp
    filename = 'reports/cmxData_{}.csv'.format(datetime.now().strftime('%Y%m%d_%H%M%S'))

    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['manufacturer', 'mac', 'lat', 'lng', 'rssi', 'seenTime']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Check if the file is empty to write the header
        if csvfile.tell() == 0:
            writer.writeheader()

        for observation in data['data']['observations']:
            lat = observation['location']['lat'] if 'location' in observation and observation['location'] else None
            lng = observation['location']['lng'] if 'location' in observation and observation['location'] else None
            writer.writerow({
                'manufacturer': observation.get('manufacturer', ''),
                'mac': observation.get('clientMac', ''),
                'lat': lat,
                'lng': lng,
                'rssi': observation.get('rssi', ''),
                'seenTime': observation.get('seenTime', '')
            })

####################################################
app = Flask(__name__)

# Respond to Meraki with validator
@app.route('/', methods=['GET'])
def get_validator():
    print("HI", request.headers)
    print("validator sent to: ",request.environ['REMOTE_ADDR'])
    requester_ip = request.headers['X-Forwarded-For']

    #Comment the line below out if you wish do not know the valid IPs(and indent correspondingly), this measure was put in place to receieve requests from multiple organizations 
    if requester_ip in valid_requester_ips: 
        print("validator for this one is:", validators[valid_requester_ips.index(requester_ip)])
    # This logic must be changed for multiple validators
    return validators[0]

# Accept CMX JSON POST
@app.route('/', methods=['POST'])
def get_cmxJSON():
    global csvfile, dayTracker, hourTracker, monthTracker, testTracker, yearTracker
    if not request.json or not 'data' in request.json:
        return("invalid data",400)
    cmxdata = request.json
    print("Received POST from ",request.environ['REMOTE_ADDR'])

    # Verify secret
    if cmxdata['secret'] not in secrets:
        print("secret invalid:", cmxdata['secret'])

        return("invalid secret",403)
    else:
        print("secret verified: ", cmxdata['secret'])

    # Verify version

    if cmxdata['version'] != version:
        print("invalid version")
        return("invalid version",400)
    else:
        print("version verified: ", cmxdata['version'])

    # Call save_data function to save the CMX data
    save_data(cmxdata)

    fileTS=''
    if summaryTimePeriod!='M':
        # check to see if it is time to generate summary
        tz = timezone(theTimeZone)
        theLocalTime = datetime.now(tz)
        #based on the timePeriod we are testing for, generate the timeStamp for the summary file if the time has come
        if summaryTimePeriod=='D':
            if dayTracker!=theLocalTime.day:
                fileTS=str(yearTracker)+'-'+str(monthTracker).zfill(2)+'-'+str(dayTracker).zfill(2)
                setTimeTrackers()
        elif summaryTimePeriod=='H':
            if hourTracker!=theLocalTime.hour:
                fileTS=str(yearTracker)+'-'+str(monthTracker).zfill(2)+'-'+str(dayTracker).zfill(2)+"-"+str(hourTracker).zfill(2)
                setTimeTrackers()
        elif summaryTimePeriod=='T':
            if testTracker!=int(theLocalTime.minute/10):
                fileTS=str(yearTracker)+'-'+str(monthTracker).zfill(2)+'-'+str(dayTracker).zfill(2)+"-"+str(hourTracker).zfill(2)+str(testTracker)
                setTimeTrackers()
        #generate the summary and rename the old detailed file only if we are in new time period
        if fileTS!='':
            # close the detailed file
            csvfile.close()
            # generateSummaryFile(fileTS)
            # re-open the file to store the raw data
            csvfile = open('cmxData.csv', 'wt')

            
    print(json.dumps(cmxdata['data'], indent=4))

    # Return success message
    return "CMX POST Received"


# Launch application with supplied arguments
def main(argv):
    global validators
    global secrets
    global csvfile
    global dayTracker, hourTracker, testTracker, monthTracker, yearTracker

    try:
       opts, args = getopt.getopt(argv,"hv:s:",["validator=","secret="])
    except getopt.GetoptError:
       print ('cmxreceiver.py -v <validator> -s <secret>')
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
           print ('cmxreceiver.py -v <validator> -s <secret>')
           sys.exit()
       elif opt in ("-v", "--validator"):
           validators.append(arg)
       elif opt in ("-s", "--secret"):
           secrets.append(arg)
    print ('validator: '+''.join(validators))
    print ('secret: '+''.join(secrets))
    print('Opening file to write out data...')

    #open the file to store the raw data
    csvfile=open('cmxData.csv', 'wt')

    #retrieve all networks from orgs
    for org in ORG_IDS:
        devices_data=getNetworks(org)
        theNetworks=json.loads(devices_data)

        #retrieve all access points from all networks to map them in memory to their corresponding network and device name
        for network in theNetworks:
            devices_data=getDevices(network['id'])
            time.sleep(0.25)
            theDevices = json.loads(devices_data)
            for device in theDevices:
                if device['model'][:2]=='MR':
                    print("========> Here is the data for just one device: ", json.dumps(device, indent=4, sort_keys=True))
                    devicesMapper[device['mac']]=network['name']
                    if 'name' in list(device.keys()) :
                        apNames[device['mac']]=device['name']
                    else :
                        apNames[device['mac']]=device['serial']

    print(devicesMapper)
    print("AP Names dict: ", apNames)
    #set the time periods where it starts to run to know when to do the summaries
    setTimeTrackers()
    print(testTracker)

if __name__ == '__main__':
    main(sys.argv[1:])
    app.run(port=5000,debug=False)
