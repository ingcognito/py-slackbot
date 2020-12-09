import os
import logging
from dotenv import load_dotenv
from flask import Flask
from slack_sdk.web import WebClient
from slackeventsapi import SlackEventAdapter
from utility import Utility

load_dotenv()
SLACK_SIGNING_SECRET=os.getenv("SLACK_SIGNING_SECRET")
SLACK_BOT_TOKEN=os.getenv("SLACK_BOT_TOKEN")

# Initialize a Flask app to host the events adapter
app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_TOKEN, "/slack/events", app)

# Initialize a Web API client
slack_web_client = WebClient(token=SLACK_BOT_TOKEN)

@slack_events_adapter.on("app_mention")
def app_mention(payload):
    """Create and send an onboarding welcome message to new users. Save the
    time stamp of this message so we can update this message in the future.
    """
    event = payload.get("event", {})
    channel_id = ["event"]["channel_id"]

    # Get the id of the Slack user associated with the incoming event
    user_id = event.get("user", {}).get("id")

    # Open a DM with the new user.
    response = slack_web_client.conversations_open(users=user_id)
    channel = response["channel"]["id"]

    # Post the onboarding message.
    start_onboarding(user_id, channel)


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(port=5000)
