import os
from dotenv import load_dotenv
import slack
from slackeventsapi import SlackEventAdapter
import spacy
import sys
import new_model

load_dotenv()
nlp = spacy.load("en_core_web_sm")

# Initialize the Slack client and event adapter
client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])
event_adapter = SlackEventAdapter(
    os.environ['SLACK_SIGNING_SECRET'], "/slack/events")

# Define the event handler for message events


@event_adapter.on("app_mention")
def handle_message(event_data):
    message = event_data["event"]
    channel_id = message["channel"]
    user_id = message.get("user")
    text = message.get("text")

    # Check if the event type is "message" and if a user sent the message
    if user_id and text:
        # Process the received message

        client.chat_postMessage(channel=channel_id, text="Working on it")
        response_text = process_message(text, chat_history)
        client.chat_postMessage(channel=channel_id, text=response_text)


def process_message(text, chat_history):
    return new_model.process_user_input(text, chat_history)


chat_history = []

# Start the Flask app
if __name__ == "__main__":

    @event_adapter.server.after_request
    def after_request(response):
        response.status_code = 200
        return response
    event_adapter.start(port=3000)
