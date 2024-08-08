import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()

def send_req(url: str, headers: dict[str, str] | None =None, data: dict[str, str] | None =None):
    while True:
        response = requests.post(url, headers=headers, json=data)
        print(response.headers)
        # If request was successful, return the response
        if response.status_code == 200:
            return response
        
        # If rate-limited, handle the 429 error
        elif response.status_code == 429:
            retry_after = response.headers.get('X-RateLimit-Reset-After')
            
            if retry_after:
                retry_after_seconds = float(retry_after)
                print(f"Rate-limited. Waiting {retry_after_seconds} seconds before retrying...")
                time.sleep(retry_after_seconds)
            else:
                print("Rate-limited, but no Retry-After header found. Waiting 10 secs before retrying...")
                time.sleep(10)
        
        else:
            # Handle other potential errors
            print(f"Request failed with status code {response.status_code}")
            response.raise_for_status()    

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
            print('Message sent successfully!')
        else:
            print(f'Failed to send message: {message_response.status_code} {message_response.text}')
    else:
        print(f'Failed to create DM channel: {response.status_code} {response.text}')
