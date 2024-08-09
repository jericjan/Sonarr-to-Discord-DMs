import threading
from files import get_file
import json
import logging
from gui import prompt_user_data


def run(skip_check: bool = False):
    json_file = get_file("data.json")
    if not json_file.exists() or skip_check:
        logging.info("No JSON file found")
        token, user_id = prompt_user_data()
        with json_file.open('w', encoding='utf-8') as f:
            json.dump({'token':token, 'user_id': user_id}, f)

def edit():
    """
    Just a threaded version of `run()`. 
    Yes, this means it runs Tkinter in a thread. 
    But hear me out, I don't even need Tkinter running all the time. 
    It kills Tkinter when it's done prompting.
    """
    t = threading.Thread(target=run, args=(True,))
    t.start()