# utils/banner.py
from pyfiglet import Figlet

def print_banner():
    f = Figlet(font="slant")  
    print(f.renderText("QT   T E S T S"))