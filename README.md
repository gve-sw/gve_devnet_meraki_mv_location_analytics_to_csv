# gve_devnet_meraki_mv_location_analytics_to_csv

Capture and process Connected Mobile Experience (CMX) data from Meraki access points. Using the Flask framework, it exposes an endpoint to receive this data in JSON format. Once received, the data is saved to a CSV file in a 'reports' directory.

## Contacts

* Rey Diaz

## Solution Components

* Meraki

## Prerequisites

#### Meraki API Keys

In order to use the Meraki API, you need to enable the API for your organization first. After enabling API access, you can generate an API key. Follow these instructions to enable API access and generate an API key:

1. Login to the Meraki dashboard
2. In the left-hand menu, navigate to `Organization > Settings > Dashboard API access`
3. Click on `Enable access to the Cisco Meraki Dashboard API`
4. Go to `My Profile > API access`
5. Under API access, click on `Generate API key`
6. Save the API key in a safe place. The API key will only be shown once for security purposes, so it is very important to take note of the key then. In case you lose the key, then you have to revoke the key and a generate a new key. Moreover, there is a limit of only two API keys per profile.

> For more information on how to generate an API key, please click [here](https://developer.cisco.com/meraki/api-v1/#!authorization/authorization).

> Note: You can add your account as Full Organization Admin to your organizations by following the instructions [here](https://documentation.meraki.com/General_Administration/Managing_Dashboard_Access/Managing_Dashboard_Administrators_and_Permissions).

## Installation / Configuration

### config.py

- **Description**: Contains configuration settings for the CMX receiver.
- **Details**:
   - `MERAKI_API_KEY`: Placeholder for the Meraki API key.
   - `ORG_IDS`: Placeholder for organization IDs.
   - `validators`: Placeholder for validators.
   - `secrets`: Placeholder for secrets.
   - `summaryTimePeriod`: Defines how often the summary is generated. For example, 'T' means every 10 minutes.
   - `version`: Determines the version of the scanning api to be used, v3 requires 3 access points for precise location scanning

### cmxreceiver.py

- **Description**: Script designed to receive CMX data from Meraki access points and save it to a CSV file.
- **Functionality**:
   - Exposes an endpoint using Flask to accept CMX data in JSON format via POST requests.
   - Verifies the secret and version of the incoming data.
   - Saves the CMX data to a CSV file in the 'reports' directory.
   - Contains functions to retrieve networks and devices from the Meraki dashboard.

## Local Machine Configuration

1. Clone the repository to your local machine.
2. Ensure you have Python installed, preferably Python 3.
3. Install the required Python packages using `pip install -r requirements.txt`.
4. Update the `config.py` file with your Meraki API key, organization IDs, validators, and secrets.

## Setting Up ngrok and Meraki Dashboard

1. Download ngrok which is used to create public URLs for programs (more information [here](https://ngrok.com)).
2. Use ngrok to expose port 5000 by entering `./ngrok http 5000` into terminal.
3. You should see a URL created that looks similar to this: `https://2a6eed03.ngrok.io/`.
4. Copy and paste this URL into the "Post URL" section of "Location and Analytics" in the Meraki Dashboard.
5. Note that the validate button should fail at this point as the CMX receiver is not up and running.

### Additional Information

- Meraki access points will listen for WiFi clients that are searching for a network to join and log the events.
- The "observations" are then collected temporarily in the cloud where additional information can be added to the event, such as GPS, X Y coordinates, and additional client details.
- Meraki will first send a GET request to this CMX receiver, which expects to receive a "validator" key that matches the Meraki network's validator.
- Meraki will then send a JSON message to this application's POST URL (i.e. `http://yourserver/` method=[POST]).
- The JSON is checked to ensure it matches the expected secret, version, and observation device type.

## Meraki Location Analytics Access Point Setup

1. Log in to your Meraki dashboard.
2. Navigate to the desired network and select the access point.
3. Under the "Location and scanning" section, enable the "Scanning API".
4. Set the POST URL to the endpoint exposed by the `cmxreceiver.py` script (e.g., `http://<your_server_ip>:5000/`).
5. Set the validator and secret as specified in the `config.py` file.

## Running the Script

1. Navigate to the repository directory on your local machine.
2. Run the `cmxreceiver.py` script using the command `python cmxreceiver.py`.
3. The Flask app will start and listen on port 5000 for incoming CMX data.
4. Send CMX data to the Flask app's endpoint to save it to a CSV file in the 'reports' directory.

# Screenshots

![/IMAGES/0image.png](/IMAGES/0image.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:

Please note: This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
