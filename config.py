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

MERAKI_API_KEY = "PLACEHOLDER_MERAKI_API_KEY"
ORG_IDS = ['PLACEHOLDER_ORG_ID'] # Replace with your organization ID
validators = ["PLACEHOLDER_VALIDATOR"] # Replace with your validator

# These are the parameters and thresholds used by the cmxsummary.py script, change as you desire
initialRSSIThreshold = 15
visitorRSSIThreshold = 10
maxSecondsAwayNewVisit = 120
minMinutesVisit = 5
theTimeZone = 'US/Central'

# How long to wait until running summary: Daily='D', Hourly='H', Test='T' (10 min interval), Manual='M'
summaryTimePeriod = 'T'  # This means every 10 minutes

secrets = ["PLACEHOLDER_SECRET"] # Replace with your secret
version = "2.0" # This code was written to support the CMX JSON version specified
