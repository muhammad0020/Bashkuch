import os
from time import sleep
from inspect import cleandoc
from collections.abc import Callable


class BaseMenu:
    """
    Abstract base class establishing the core interface for system menus.

    This class provides the blueprint and shared foundational utilities for
    rendering user interfaces, capturing input, and orchestrating menu-driven
    application workflows.
    """
    @staticmethod
    def clear_terminal(delay: int=0):
        """
        Clears terminal screen after specified delay (default: 0 seconds).

        Parameters:
            - delay: Seconds to wait before clearing terminal.
        """
        sleep(delay)
        # Use 'cls' on Windows, 'clear' on Unix-like systems to clear the screen.
        os.system("cls" if os.name == "nt" else "clear")

    @staticmethod
    def show_header(title: str):
        """
        Displays program header for menus.

        Parameters:
            - title: Title of current menu.
        """
        print("=" * 46)
        print(f"|{title.center(44)}|")
        print("=" * 46)

    @classmethod
    def show_message(cls, message: str):
        """
        Prints message and auto-clears screen after delay (default: 2 seconds).

        Parameters:
            - message (str): Specific message to center in frame.
        """
        print("=" * 46)
        print(f"|{message.center(44)}|")
        print("=" * 46)
        print()
        cls.clear_terminal(2)

    @staticmethod
    def _show_menu(options: dict | list | tuple):
        """Displays menu options for current function."""
        print("=" * 46)
        for row, option in enumerate(options, start=1):
            print(f"|{row}.{option:<42}|")
        print("=" * 46)

    @staticmethod
    def _validate_menu_selection(user_input: str, limit: int) -> bool:
        """
        Validate and convert user input to an integer within a specified range.

        Attempts to parse the input string as an integer and checks if it falls
        within the interval (0, limit]. Serves as a helper for menu selection validation.

        Parameters:
            user_input: Raw string entered by the user (e.g., "3").
            limit: Maximum allowed value (inclusive). Minimum is always 1.

        Returns:
            bool:
                - True: If input is an integer between 1 and limit.
                - False: If input is not an integer or is out of range.
        """
        return user_input.isdecimal() and 0 < int(user_input) <= limit

    @classmethod
    def capture_menu_selection(cls, options: dict | list | tuple, prompt: str,
                               error: str="Invalid input", *, convert_to_index: bool=False) -> int:
        """
        Display a menu, prompt the user, and return a validated integer choice.

        This class method renders the given options (dictionary, list, or tuple),
        repeatedly asks for input until a valid selection within the available
        range is entered, and optionally converts the 1‑based user choice to
        a 0‑based index.

        Parameters:
            options: A collection of menu items to display.
                     - If a dict, keys are used as option identifiers.
                     - If a list or tuple, the items are shown as numbered options.
            prompt: The message displayed to the user for input.
            error: Optional error message shown when validation fails.
                   Defaults to "Invalid input".
            convert_to_index: If True, returns the choice minus 1 (0‑based index);
                              otherwise returns the raw 1‑based integer choice.
                              Defaults to False.

        Returns:
            int: A valid integer representing the user's choice. If convert_to_index
                 is True, the returned value is in the range [0, len(options)-1];
                 otherwise it is in the range [1, len(options)].
        """
        cls._show_menu(options)
        while True:
            choice = input(cleandoc(prompt))
            if cls._validate_menu_selection(choice, len(options)):
                choice = int(choice)
                return (choice - 1) if convert_to_index else choice
            cls.show_message(error)

    def get_validated_string(self, prompt: str, errors: tuple[str, str],
                             *, validator: Callable[[str], str], transform: bool=True) -> str:
        """
        Repeatedly prompt the user for a string input until it passes validation.

        The input is stripped of whitespace and converted to lowercase before being
        passed to the validator function. Based on the validator's return value,
        the method either returns the validated string or displays an appropriate
        error message and retries.

        Parameters:
            prompt: The message displayed to the user when asking for input.

            errors: A tuple of two error messages:
                - errors[0] is shown when the validator returns 'empty' (empty input).
                - errors[1] is shown when the validator returns 'too_long' (input exceeds the limit).

            validator: A callable that takes a single string argument and returns:
                - 'success': if the input is valid
                - 'empty': if the input is empty
                - 'too_long': if the input exceeds the limit.

            transform:
                - True (default): the input is stripped of leading/trailing whitespace
                   (spaces, tabs, newlines) and converted to lowercase. Use this for
                   service names and usernames where case and surrounding spaces are not
                   significant.

                - False: only the trailing newline character is removed (with .rstrip('\n'))
                   and all other whitespace (leading/trailing spaces, tabs) is preserved.
                   This is necessary for passwords where spaces, tabs, or other whitespace
                   characters may be intentionally part of the secret.

       Returns:
            The validated string entered by the user. If transform was True, the string
            has been stripped of leading/trailing whitespace and converted to lowercase.
            If transform was False, only the trailing newline character is removed and
            all other whitespace (including leading/trailing spaces/tabs) is preserved.
        """
        while True:
            user_input = input(prompt)
            status = validator(user_input)
            if status == "success":
                if transform:
                    # Replaces internal tab characters with spaces to clean mid-string input,
                    # then utilizes .strip() to eliminate any leading/trailing whitespace.
                    return user_input.replace("\t", " ").strip().lower()
                else:
                    # Keep the password data 100% raw and untouched to preserve user secrets.
                    return user_input
            elif status == "empty":
                self.show_message(errors[0])
            elif status == "too_long":
                self.show_message(errors[1])