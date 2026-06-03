"""Functions execute in main.py"""

from .core import AccountManager
from .core.manage_accounts import manage_passwords
from .core.generate_password import password_generator
from .core.delete_accounts import recycle_bin

from .ui import AccountCreatorMenu

from .utils.manage_data import load_data
from .common import BaseMenu
from .common import menu_titles, menu_options, messages