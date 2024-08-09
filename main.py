import pystray # type: ignore
from PIL import Image
from pathlib import Path
from server import app
import logging
import threading
import subprocess

def get_file(name: str) -> Path:
    return Path(__file__).resolve().parent / name 

logging.basicConfig(filename=str(get_file('output.log')), level=logging.INFO)

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
    pystray.MenuItem('Exit', lambda : exit_app(icon)),    
)
icon.icon = img
icon.title = "Sonnar to Discord DMs"

def setup(icon: pystray._base.Icon): # type: ignore
    icon.visible = True
    logging.info("Starting flask server")    
    thread = threading.Thread(target=lambda: app.run(debug=False), daemon=True)
    thread.start()

icon.run(setup) # type: ignore
print("Exiting...")