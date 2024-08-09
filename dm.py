import requests
import os
from dotenv import load_dotenv
import time
import logging




load_dotenv()

def send_req(url: str, headers: dict[str, str] | None =None, data: dict[str, str] | None =None):
    while True:
        try:
            response = requests.post(url, headers=headers, json=data)
        except requests.exceptions.RequestException:
            logging.info("Something went wrong. Trying again in 5 secs")
            time.sleep(5)
            continue

        # If request was successful, return the response
        if response.status_code == 200:
            return response
        
        # If rate-limited, handle the 429 error
        elif response.status_code == 429:
            retry_after = response.headers.get('X-RateLimit-Reset-After')
            
            if retry_after:
                retry_after_seconds = float(retry_after)
                logging.info(f"Rate-limited. Waiting {retry_after_seconds} seconds before retrying...")
                time.sleep(retry_after_seconds)
            else:
                logging.info("Rate-limited, but no Retry-After header found. Waiting 10 secs before retrying...")
                time.sleep(10)
        
        else:
            # Handle other potential errors
            logging.info(f"Request failed with status code {response.status_code}. Trying again in 10 secs.")
            time.sleep(10)

def do_dm(message: str):
    # Your bot token here
    TOKEN = os.getenv("TOKEN")

    # The ID of the user you want to send a DM to
    USER_ID = os.getenv("USER_ID")

    # Discord API endpoint to create a DM channel
    dm_url = 'https://discord.com/api/v10/users/@me/channels'

    # Headers with the authorization token
    headers = {
        'Authorization': f'Bot {TOKEN}',
        'Content-Type': 'application/json'
    }

    # Create a DM channel with the user
    dm_data = {
        'recipient_id': USER_ID
    }

    response = requests.post(dm_url, headers=headers, json=dm_data)

    # Check if the channel was created successfully
    if response.status_code == 200:
        dm_channel_id = response.json()['id']
        
        # Now send a message to the DM channel
        message_url = f'https://discord.com/api/v10/channels/{dm_channel_id}/messages'
        message_data = {
            'content': message
        }
        
        message_response = send_req(message_url, headers, message_data)
        
        if message_response.status_code == 200:
            logging.info('Message sent successfully!')
        else:
            logging.error(f'Failed to send message: {message_response.status_code} {message_response.text}')
    else:
        logging.error(f'Failed to create DM channel: {response.status_code} {response.text}')
