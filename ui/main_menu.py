"""
Defines the application's main menu.

Presents the top-level menu options and directs users
to the appropriate application workflows.
"""

from .base_menu import BaseMenu
from .creator_menu import AccountCreatorMenu
from .generator_menu import PasswordGeneratorMenu


class MainMenu(BaseMenu):
    """Represents the application's primary navigation menu."""

    def __init__(self, manager):
        self.manager = manager
        self.title = "BASHKUCH"
        self.options = {
            "main": ("Add account", "Manage accounts", "Generate password", "Recycle bin", "Exit"),
            "exit": ("No, Back to app", "Yes, Exit the app")
        }
        self.prompts = {
            "choice": "Choose an option:",
            "exit": "Are you sure you want to exit?:"
        }

    def run(self) -> BaseMenu | None:
        """
        Displays options, captures user input, and determines the next navigation state.

        Renders the main menu interface to the terminal, captures the user's choice,
        and validates the input. To drive the return-based navigation stack in the
        orchestrator layer, it returns one of two distinct signal types.

        Returns:
            BaseMenu: An instance of the next menu to push onto the navigation stack.
            None: To pop the current menu and navigate backward.
        """
        while True:
            self.show_header(self.title)
            choice = self.capture_menu_selection(self.options["main"],
                                                 self.prompts["choice"],
                                                 allow_navigation_back=False)
            if choice == 1:
                return AccountCreatorMenu(self.manager)
            elif choice == 2:
                self.show_message("This feature is temporarily unavailable.")
            elif choice == 3:
                return PasswordGeneratorMenu()
            elif choice == 4:
                self.show_message("This feature is temporarily unavailable.")
            else:
                exit_decision = self.capture_menu_selection(self.options["exit"],
                                                            self.prompts["exit"],
                                                            allow_navigation_back=False)
                self.clear_terminal()
                if exit_decision == 2:
                    return None
