import logging
import subprocess
import sys
import threading
from tkinter.messagebox import showinfo as popup  # type: ignore

import pystray  # type: ignore
from PIL import Image
from waitress import serve

import data_setup
from files import get_data, get_file
from ports import port_available
from server import app

file_handler = logging.FileHandler(filename=str(get_file("output.log")))
stdout_handler = logging.StreamHandler(stream=sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(handlers=handlers, level=logging.INFO)

setup_success = data_setup.run()

if setup_success == False:
    logging.info("First time setup failed. Exiting program.")
    get_file("data.json").unlink()
    exit()

logging.info("Setup succeeded")


def exit_app(icon: pystray._base.Icon):  # type: ignore
    icon.visible = False
    logging.info("Exiting")
    icon.stop()


def find_log():
    subprocess.Popen(f"explorer.exe /select,{get_file('output.log')}")


img = Image.open(get_file("icon.png"))
icon = pystray.Icon("icon")
icon.menu = pystray.Menu(
    pystray.MenuItem("Open log file", find_log),
    pystray.MenuItem("Edit data", data_setup.edit),
    pystray.MenuItem("Exit", lambda: exit_app(icon)),
)
icon.icon = img
icon.title = "Sonnar to Discord DMs"


def setup(icon: pystray._base.Icon):  # type: ignore
    icon.visible = True
    logging.info("Starting flask server")
    default_port = 5000
    data = get_data()
    if data is None:
        port = default_port
    else:
        port = data.get('port', default_port)
    port = int(port)
    if port_available(port):        
        thread = threading.Thread(
            target=lambda: serve(app, host="0.0.0.0", port=port), daemon=True
        )
        thread.start()
    else:
        popup("Uh oh", f"Port {port} is in use! Please try a different one")
        exit_app(icon)


icon.run(setup)  # type: ignore
print("Exiting...")
