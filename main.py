from terminal_interface import terminal_ui
from src.ui.flet_app import start_flet_app

interface = "flet"

if interface == "terminal":
    terminal_ui()
elif interface == "flet":
    start_flet_app()
