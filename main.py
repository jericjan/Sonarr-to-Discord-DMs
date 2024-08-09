import pystray # type: ignore
from PIL import Image
import data_setup
from ports import port_available
from server import app
import logging
import threading
import subprocess
from files import get_file
import sys
from waitress import serve
from tkinter.messagebox import showinfo as popup # type: ignore

file_handler = logging.FileHandler(filename=str(get_file('output.log')))
stdout_handler = logging.StreamHandler(stream=sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(handlers=handlers, level=logging.INFO)

data_setup.run()

def exit_app(icon: pystray._base.Icon): # type: ignore
    icon.visible = False
    logging.info("Exiting")
    icon.stop()
    
def find_log():
    subprocess.Popen(f"explorer.exe /select,{get_file('output.log')}")

img = Image.open(get_file("icon.png"))
icon = pystray.Icon('icon')
icon.menu =pystray.Menu(
    pystray.MenuItem('Open log file', find_log),
    pystray.MenuItem('Edit data', data_setup.edit),
    pystray.MenuItem('Exit', lambda : exit_app(icon)),    
)
icon.icon = img
icon.title = "Sonnar to Discord DMs"

def setup(icon: pystray._base.Icon): # type: ignore
    icon.visible = True
    logging.info("Starting flask server")
    port = 5000
    if port_available(port):
        thread = threading.Thread(target=lambda: serve(app, host="0.0.0.0", port=5000), daemon=True)
        thread.start()
    else:
        popup("Uh oh", f"Port {port} is in use! Please try a different one")
        exit_app(icon)
icon.run(setup) # type: ignore
print("Exiting...")