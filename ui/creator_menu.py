"""
Provides the AccountCreatorMenu implementation for creating
new accounts through the application's menu system.
"""

from .base_menu import BaseMenu


class AccountCreatorMenu(BaseMenu):
    """
    Interactive menu for creating a new account (service name, username, password).

    This class handles user input collection, validation, duplicate checking,
    and delegation of account creation to the central manager. It inherits common
    UI methods (clear_terminal, show_header, show_message) from BaseMenu.

    Attributes:
        - manager (MenuManager): The main manager instance providing shared resources
                               such as validation, key checking, and account storage.
        - title (str): Header title displayed when the menu is shown.
        - success (dict): Success messages displayed after successful operations.
        - prompts (dict): Input prompts for 'service_name', 'username', 'password'.
        - errors (dict): Error messages for empty, too long, or duplicate entries.
    """
    def __init__(self, manager):
        self.manager = manager
        self.title = "CREATE ACCOUNTS"
        self.success = {"saved": "Account information saved!"}
        self.prompts = {
            "service_name": "Enter service name:",
            "username": "Enter username: ",
            "password": "Enter password: "
        }
        self.errors = {
            "empty_service_field": "Service name cannot be empty!",
            "empty_username_field": "Username cannot be empty!",
            "empty_password_field": "Password field cannot be empty!",
            "too_long_service_name": "Service name cannot exceed 30 characters.",
            "too_long_username": "Username cannot exceed 30 characters.",
            "too_long_password": "Password cannot exceed 30 characters.",
            "exist": "This service with this username is already exist"
        }

    def run(self):
        """
        Execute the account creation workflow.

        Prompts the user for service name, username, and password repeatedly
        until valid input is provided. It ensures:
          - Service name and username are unique together (via manager.check_key).
          - All fields respect length limits (using manager.length_validation).
          - Password input preserves whitespace (transform=False).
        On successful creation, clears the terminal, displays a confirmation
        message, and returns to the previous menu.
        """
        self.show_header(self.title)
        while True:
            service_name = self.get_validated_string(self.prompts["service_name"],
                                                     (self.errors["empty_service_field"],
                                                      self.errors["too_long_service_name"]),
                                                     validator=self.manager.length_validation)

            username = self.get_validated_string(self.prompts["username"],
                                                 (self.errors["empty_username_field"],
                                                  self.errors["too_long_username"]),
                                                 validator=self.manager.length_validation)

            key = (service_name, username)
            if self.manager.check_key(key):
                self.show_message(self.errors["exist"])
                continue
            password = self.get_validated_string(self.prompts["password"],
                                                 (self.errors["empty_password_field"],
                                                  self.errors["too_long_password"]),
                                                 validator=self.manager.length_validation, transform=False)
            self.manager.create_accounts(service_name, username, password, key)
            self.clear_terminal()
            self.show_message(self.success["saved"])
            return
