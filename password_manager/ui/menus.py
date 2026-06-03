from ..utils import BaseMenu

class AccountCreatorMenu(BaseMenu):
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