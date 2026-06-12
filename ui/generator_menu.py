from core.password_generator import generate_secure_password, length_validation
from utils import copy_to_clipboard
from .base_menu import BaseMenu


class PasswordGeneratorMenu(BaseMenu):
    """
    Interactive menu for generating secure passwords.

    Allows users to generate cryptographically secure passwords,
    display them, and optionally copy them to the system clipboard.
    """
    MINIMUM_LENGTH = 8
    MAXIMUM_LENGTH = 24
    TITLE = "GENERATE PASSWORDS"
    OPTIONS = ("Generate another password", "Copy password to clipboard")
    PROMPTS = {
            "choose_option": "Choose an option: ",
            "ask_length": "How long should the password be?"
        }
    SUCCESS_MESSAGES = {"copy_success": "Password copied to clipboard!"}
    ERROR_MESSAGES = {
            "copy_failed": "Copy failed. Try selecting the text manually.",
            "invalid_length": f"Password must be {MINIMUM_LENGTH}-{MAXIMUM_LENGTH} chars long"
        }

    def run(self) -> BaseMenu | None:
        """
        Execute the password generator menu workflow.

        Prompts the user for a password length, validates the input,
        generates a secure password, and presents available actions
        such as generating another password or copying the generated
        password to the clipboard.

        Returns:
        - The next menu to navigate to, or None if
          the menu should be closed.
        """
        self.show_header(self.TITLE)
        while True:
            password_length = input(self.PROMPTS["ask_length"])
            if password_length.strip().lower() == self.NAVIGATE_BACK_KEY:
                return

            if not length_validation(password_length, self.MINIMUM_LENGTH, self.MAXIMUM_LENGTH):
                self.show_message(self.ERROR_MESSAGES["invalid_length"])
                continue
            generated_password = generate_secure_password(int(password_length))
            self.show_message(generated_password)
            choice = self.capture_menu_selection(self.OPTIONS, self.PROMPTS["choose_option"])

            if choice == 1:
                continue

            elif choice == 2:
                if copy_to_clipboard(generated_password):
                    self.show_message(self.SUCCESS_MESSAGES["copy_success"])
                else:
                    self.show_message(self.ERROR_MESSAGES["copy_failed"])
                continue
            return


