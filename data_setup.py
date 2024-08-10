from files import get_file, save_data
import logging
from gui import prompt_user_data


def run(edit: bool = False):
    json_file = get_file("data.json")
    success = True
    if not json_file.exists():  # Opened for the first time
        save_data({"token": "", "user_id": "", "port": "5000"})
        logging.info("No JSON file found")
        try:
            token, user_id, port = prompt_user_data()
            save_data({"token": token, "user_id": user_id, "port": port})
        except Exception as e:
            logging.info(e)
            success = False
    elif edit is True:  # File exists and user is editing
        logging.info("Opened window for editing data")
        try:
            token, user_id, port = prompt_user_data()
            save_data({"token": token, "user_id": user_id, "port": port})
        except Exception as e:
            logging.info(e)
    return success
