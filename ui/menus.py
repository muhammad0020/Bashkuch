from utils import BaseMenu

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


class AccountEditorMenu(BaseMenu):
    """
    Provide an interactive menu to edit service name, username, or password of a selected account.

    This class manages the user interface for editing a specific account's fields.
    It displays the current values, prompts for new input, validates using a central
    validator, and updates the account dictionary. It also handles unique service name and username
    constraints and success/error messaging.

    Attributes:
        account (dict): The account dictionary to be edited. Expected keys:
                        'service_name', 'username', 'password'.
        manager (AccountManager): An instance of the account manager that provides
                               logic methods like edit_account, length_validation
                               and access to unique_keys set for duplicate checking.

    Usage:
        menu = EditAccountMenu(account, manager)
        menu.run()
    """
    def __init__(self, account: dict, manager):
        self.account = account
        # Store account keys dynamically to avoid hardcoding string keys in methods.
        # This ensures the code remains flexible if dictionary key names change later.
        self.account_keys = list(self.account.keys())
        self.manager = manager
        self.title = "EDIT ACCOUNTS"
        self.options = ("Edit service name", "Edit username", "Edit password", "Back to previous menu")
        self.prompts = {
            "choice": "Choose an option: ",
            "new_service": "Enter new service name: ",
            "new_username": "Enter new username: ",
            "new_password": "Enter new password: ",
        }
        self.success = {
            "service_updated": "Service name updated!",
            "username_updated": "Username updated!",
            "password_updated": "Password updated!"
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

    def _edit_account_data(self, prompt: str,
                           errors: tuple[str, str],
                           success_msg: str,
                           key: str,
                           *, unique_key_update: bool=True):
        """
         Edit a specific field of an account.

        This method prompts the user for a new value, validates it using the provided
        validator, and updates the account dictionary at the given key.

        Parameters:
            prompt: The message shown to the user when asking for input.
            errors: A tuple of two strings:
                - errors[0]: displayed when input is empty.
                - errors[1]: displayed when input exceeds the length limit.
            success_msg: Message shown after the field is successfully updated.
            key: The dictionary key of the field to edit (e.g., 'service_name', 'username', 'password').
            unique_key_update: If True, the internal unique_keys set will be updated
                               (used when changing 'service_name' and 'username' to maintain uniqueness).
        """
        new_value = self.get_validated_string(prompt, errors, validator=self.manager.length_validation)
        if key == self.account_keys[0]:
            has_duplicated = self.manager.check_key((new_value, self.account[self.account_keys[1]]))
        elif key == self.account_keys[1]:
            has_duplicated = self.manager.check_key((self.account[self.account_keys[0]], new_value))
        else:
            has_duplicated = False  # password change doesn't need duplication check

        if not has_duplicated:
            self.manager.edit_account(self.account, new_value, key=key, unique_key_update=unique_key_update)
            self.show_message(success_msg)
        else:
            self.show_message(self.errors["exist"])

    def run(self):
        """
        Executes the interactive menu loop for editing account fields.

        This method displays the interface header and continuously captures user
        input to modify specific account attributes (service name, username, or
        password). It dynamically maps menu choices to database fields using the
        internal keys array. The loop terminates when the user selects the exit option.
        """
        self.show_header(self.title)

        while True:
            choice = self.capture_menu_selection(self.options, self.prompts["choice"])

            if choice == 1:
                self._edit_account_data(self.prompts["new_service"],
                                        (self.errors["empty_service_field"],
                                        self.errors["too_long_service_name"]),
                                        self.success["service_updated"],
                                        key=self.account_keys[0])

            elif choice == 2:
                self._edit_account_data(self.prompts["new_username"],
                                        (self.errors["empty_username_field"],
                                        self.errors["too_long_username"]),
                                        self.success["username_updated"],
                                        key=self.account_keys[1])

            elif choice == 3:
                self._edit_account_data(self.prompts["new_password"],
                                        (self.errors["empty_password_field"],
                                        self.errors["too_long_password"]),
                                        self.success["password_updated"],
                                        key=self.account_keys[2],
                                        unique_key_update=False)
            else:
                break


