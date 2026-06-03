"""
Generates a secure random password containing at least
one uppercase, one lowercase, one digit, and one symbol character.

Password length is configurable and meets security standards.

Ensures diversity to prevent common attacks.
"""

import string
import random

from ..common import BaseMenu
from ..common import menu_titles, menu_options, messages
from ..utils.manage_data import copy_to_clipboard


def password_generator():
    """Generate a random password and check if the password is strong."""

    def generate_password(length=16):
        """
        Generate a random password.

        Parameters:
            - length (int): Length of the password (Optional, Defaults to 16).
        """

        chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(chars) for _ in range(length))


    def is_password_strong(password):
        """
        Check if the password is strong or not.

        Parameters:
            - password (str): Generated password to check.

        Returns:
            - bool:
                * True: if password has all character types (uppercase and lowercase letters, digits and symbols).
                * False: if password hasn't all character types.
        """

        has_upper = False
        has_lower = False
        has_digit = False
        has_symbol = False

        for char in password:
            if char in string.ascii_uppercase:
                has_upper = True

            if char in string.ascii_lowercase:
                has_lower = True

            if char in string.digits:
                has_digit = True

            if char in string.punctuation:
                has_symbol = True

        return has_upper and has_lower and has_digit and has_symbol

    password_creator = BaseMenu()
    while True:
        generated_password = generate_password()

        # Ensure password has all character types (retries on failure)
        if not is_password_strong(generated_password):
            continue
        password_creator.show_header(menu_titles["generate"])
        print(f"Generated password:   {generated_password}")

        selection = password_creator.capture_menu_selection(menu_options["generate"]["main"], messages["prompt"]["choice"])
        if selection == 1:  # Generate another password
            continue

        elif selection == 2:
            copy_to_clipboard(generated_password)
            option = password_creator.capture_menu_selection(menu_options["generate"]["after_copy"], messages["prompt"]["choice"])
            if option == 1:
                continue

            else:  # exit to main
                return

        else:  # exit to main
            return