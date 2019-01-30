#Adopted with modifications from https://github.com/mattmakai/slack-starterbot/blob/master/starterbot.py
#Distributed under MIT license

#don't forget to set the environmental variable SLACK_BOT_TOKEN using
#export SLACK_BOT_TOKEN='Your Bot User OAuth Access Token'
#or hardcode 

import os
import time
import re
from slackclient import SlackClient
import requests

import json #used for debug printing

OAUTH_TOKEN = 'INSERT TOKEN HERE' #DO NOT COMMIT TOKEN
WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/'
WEATHER_API_KEY = 'INSERT KEY HERE' #DO NOT COMMIT API KEY

# instantiate Slack client
slack_client = SlackClient(OAUTH_TOKEN)
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
MENTION_REGEX = "^<@(|[WU].+)>(.*)"
WEATHER_REGEX = r"\s*((what|how)\s+)?(is\s+)?(the\s+)?weather\s+(in\s+)?(?P<city>.*)\?\s*"

def kelvin_to_celcius(kelvin):
    return kelvin - 273.15

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
    	#uncomment line below to debug print
        print(json.dumps(event, indent = 2, sort_keys = True))
        
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            #uncomment line below to debug print
            print("user id  = {} : message = {}".format(user_id, message))
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "I only answer questions."

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    if command.strip().endswith('?'):
        m = re.match(WEATHER_REGEX, command)
        print(m)
        if m:
            city = m.group('city')
            url = f"{WEATHER_API_URL}weather?q={city}&APPID={WEATHER_API_KEY}"
            res = requests.get(url)
            jsonRes = res.json()
            resCode = int(jsonRes['cod'])

            if resCode >= 200 and resCode <= 299:
                description = jsonRes['weather'][0]['description']
                temperature = kelvin_to_celcius(jsonRes['main']['temp'])
                response = f'Expect {description} in {city} with a temperature of {temperature}°C.'
            else:
                response = f'I HAVE FAILED YOU ;_; (Response Code: {resCode})'
        else: 
            response = command
        

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

if __name__ == "__main__":
	# avm: connect is designed for larger teams, 
	# see https://slackapi.github.io/python-slackclient/real_time_messaging.html
	# for details
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")