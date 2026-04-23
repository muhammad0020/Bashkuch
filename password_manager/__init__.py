"""Functions execute in main.py"""

from .core.add_accounts import add_password
from .core.manage_accounts import manage_passwords
from .core.generate_password import password_generator
from .core.delete_accounts import recycle_bin

from .utils.manage_data import load_data
from .common import show_header, show_and_get, clear_terminal
from .common import menu_titles, menu_options, messages