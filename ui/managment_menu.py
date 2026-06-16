"""
Account Management Console Module.

This module provides a CLI-based system for managing user accounts,
including viewing, searching, deleting, restoring, and
permanently removing accounts.

Key Features:
    - Account listing and selection menus
    - Search functionality with result navigation
    - Soft delete (recycle bin) and hard delete operations
    - Account restoration from recycle bin
    - Centralized account state management via AccountManager

Architecture:
    - Menu-based navigation system using BaseMenu
    - State-driven flows via AccountState
    - Separation of UI logic (menus) and business logic (AccountManager)

Note:
    This module is designed as a console interface and may be
    replaced or migrated to a web-based interface (e.g., Flask)
    in future development stages.
"""

from inspect import cleandoc
from enum import Enum, auto

from .base_menu import BaseMenu
from .editor_menu import AccountEditorMenu
from navigation import NavigateTwoStepsBack


class AccountState(Enum):
    """
    Represents the account category currently being managed.

    Members:
        ACTIVE_ACCOUNTS:
            Indicates that operations are being performed on
            active accounts.

        DELETED_ACCOUNTS:
            Indicates that operations are being performed on
            accounts stored in the recycle bin.
    """
    ACTIVE_ACCOUNTS = auto()
    DELETED_ACCOUNTS = auto()


class AccountManagerMenu(BaseMenu):
    """
    Handles the main menu for managing user accounts.

    This menu operates in two modes based on AccountState:
    - ACTIVE_ACCOUNTS: manages active user accounts
    - DELETED_ACCOUNTS: manages accounts in the recycle bin

    Responsibilities:
        - Display appropriate menu options based on account state
        - Route user actions to account search, selection, or deletion flows
        - Provide access to account-related operations via AccountManager
    """
    PROMPTS = {"choose_option": "Choose an option: "}

    def __init__(self, manager, state: AccountState):
        self.manager = manager
        self.state = state
        if self.state == AccountState.ACTIVE_ACCOUNTS:
            self.main_list = self.manager.active_accounts
            self.title = "MANAGE ACCOUNTS"
            self.options = ("Search services", "Show saved accounts")
            self.error_messages = {"no_account": "No accounts saved!"}

        else:
            self.main_list = self.manager.deleted_accounts
            self.title = "RECYCLE BIN"
            self.options = ("Empty recycle bin", "Show deleted accounts")
            self.error_messages = {"no_account": "Recycle bin is empty!"}

    def run(self) -> BaseMenu | None:
        """
       Executes the account management menu workflow.

       Flow:
           - If no accounts exist in the current context, an error message is shown.
           - Displays menu options based on account state.
           - Processes user selection:
               * Search accounts (active state only)
               * Show account list
               * Empty recycle bin (deleted state only)

       Returns:
           BaseMenu:
               Next menu in the navigation flow (Search, Select, or Delete operations)

           None:
               If no accounts are available or the menu is exited.
        """
        if not self.main_list:
            self.show_message(self.error_messages["no_account"])
            return None

        self.show_header(self.title)
        while True:
            choice = self.capture_menu_selection(self.options, self.PROMPTS["choose_option"])
            if choice == 1:
                if self.state == AccountState.ACTIVE_ACCOUNTS:
                    return SearchAccountsMenu(self.manager)
                return DeleteAllAccountsMenu(self.manager)

            else:
                if self.state == AccountState.ACTIVE_ACCOUNTS:
                    return SelectAccountMenu(self.main_list, self.manager, self.state)
                return SelectAccountMenu(self.main_list, self.manager, self.state)


class SearchAccountsMenu(BaseMenu):
    """
    Handles the account search input flow.

    This menu is responsible for:
        - Receiving a search query from the user
        - Handling navigation back to the previous menu
        - Forwarding the search query to SearchResultsMenu
    """
    PROMPTS = {"search_prompt": "Enter account name to start searching: "}
    def __init__(self, manager):
        self.manager = manager

    def run(self) -> BaseMenu | None:
        """
        Prompts the user for an account name and initiates a search operation.

        Flow:
            - Continuously prompts the user for a search query
            - If the back navigation key is entered, exits the menu
            - Otherwise, forwards the search query to SearchResultsMenu

        Returns:
            BaseMenu:
                SearchResultsMenu initialized with the search query.

            None:
                If the user chooses to navigate back.
        """
        while True:
            print("=" * 46)
            search_query = input(self.PROMPTS["search_prompt"]).strip().lower()
            if search_query == self.NAVIGATE_BACK_KEY:
                return None
            return SearchResultsMenu(self.manager, search_query)


class SearchResultsMenu(BaseMenu):
    """
    Displays search results and allows the user to select an account.

    Responsibilities:
        - Executes account search based on user query
        - Displays matching accounts
        - Handles empty results and navigation fallback
        - Forwards selected account to details view
    """
    PROMPT = {"choose_account": "Choose an account: "}
    ERROR_MESSAGES = {"not_found": "This account with this name doesn't exist!"}
    def __init__(self, manager, search_query: str):
        self.manager = manager
        self.search_query = search_query

    def run(self) -> BaseMenu | None:
        """
        Runs the search results menu workflow.

        Flow:
            - If no active accounts exist, navigates back two steps
            - Searches accounts based on the provided query
            - If no results found, shows error message and exits
            - Otherwise displays results and allows user selection
            - Opens account details for the selected account

        Returns:
            - BaseMenu: ShowAccountDetails for the selected account.
            - None: If no results are found or user exits.
        """
        if not self.manager.active_accounts:
            raise NavigateTwoStepsBack
        search_results = self.manager.search_accounts(self.search_query)
        if not search_results:
            self.show_message(self.ERROR_MESSAGES["not_found"])
            return None
        index = self.capture_menu_selection(search_results, self.PROMPT["choose_account"], convert_to_index=True)
        selected_account = search_results[index]
        return ShowAccountDetails(selected_account, self.manager, AccountState.ACTIVE_ACCOUNTS)


class SelectAccountMenu(BaseMenu):
    """
   Displays a list of accounts and allows the user to select one.

   This menu is used to show a predefined list of accounts and
   forward the selected account to the details view.

   Attributes:
       - accounts: The list of account dictionaries to display.
       - manager: Reference to AccountManager for shared operations.
       - state: The current AccountState used in downstream navigation.
    """
    PROMPT = {"choose_account": "Choose an account: "}
    def __init__(self, accounts: list[dict], manager, state: AccountState):
        self.manager = manager
        self.accounts = accounts
        self.state = state

    def run(self) -> BaseMenu | None:
        """
        Executes the account selection flow.

        Flow:
            - If the account list is empty, exits the menu.
            - Displays available accounts to the user.
            - Captures user selection.
            - Returns a ShowAccountDetails menu for the selected account.

        Returns:
            - ShowAccountDetails: Menu displaying detailed information for the selected account.
            - None: If no accounts are available or user exits.
        """
        if not self.accounts:
            return None
        index = self.capture_menu_selection(self.accounts, self.PROMPT["choose_account"], convert_to_index=True)
        selected_account = self.accounts[index]
        return ShowAccountDetails(selected_account, self.manager, self.state)


class ShowAccountDetails(BaseMenu):
    """
    Displays detailed information for a selected account
    and handles user actions on that account.

    Responsibilities:
       - Show account details (service, username, password)
       - Present available actions based on AccountState
       - Route user actions to edit, delete, or restore flows
    """
    PROMPTS = {"choose_option": "choose an option"}
    def __init__(self, account: dict, manager, state: AccountState):
        self.account = account
        self.manager = manager
        self.state = state
        if self.state == AccountState.ACTIVE_ACCOUNTS:
            self.options = ("Edit information", "Delete account")

        else:
            self.options = ("Restore account", "Delete account")

    def run(self) -> BaseMenu:
        """
        Displays account details and processes user actions.

        Flow:
            - Prints selected account information
            - Shows available options based on account state
            - Handles user selection:
                * Edit account (active accounts only)
                * Delete account
                * Restore account (deleted accounts only)

        Returns:
            - BaseMenu: Next menu based on user action (edit, delete, restore).
        """
        print("=" * 46)
        print(cleandoc(f"""
            Service name: {self.account["service_name"]}  
            Username: {self.account["username"]}   
            Password: {self.account["password"]}
            """))
        print("=" * 46)
        choice = self.capture_menu_selection(self.options, self.PROMPTS["choose_option"])
        if self.state == AccountState.ACTIVE_ACCOUNTS:
            if choice == 1:
                return AccountEditorMenu(self.account, self.manager)
            return DeleteAccountMenu(self.account, self.manager, self.state)

        else:
            if choice == 1:
                return RestoreAccountMenu(self.account, self.manager)
            return DeleteAccountMenu(self.account, self.manager, self.state)


class RestoreAccountMenu(BaseMenu):
    """
    Handles restoring a deleted account back to active accounts.

    This menu is responsible for:
        - Validating that the account does not already exist
        - Restoring the account from deleted to active list
        - Updating unique account keys to prevent duplicates
        - Handling success and error feedback to the user
    """
    SUCCESS_MESSAGES = {"data_restored": "Data restored!"}
    ERROR_MESSAGES = {"exist": "This service with this username is already exist"}
    def __init__(self, account, manager):
        self.account = account
        self.manager = manager

    def run(self) -> None:
        """
        Restores a deleted account to the active accounts list if possible.

        Flow:
            - Creates a unique key from account service name and username
            - Checks if an account with the same key already exists
            - If no duplicate exists:
                * Transfers account from deleted to active list
                * Registers the account key
                * Shows success message
                * Navigates two steps back in menu flow
            - If duplicate exists:
                * Shows error message
                * Back to previous menu

        Returns:
            - None: If restoration fails due to duplicate account.
        """
        deleted_keys = (self.account["service_name"], self.account["username"])
        has_duplicated = self.manager.check_key(deleted_keys)
        if not has_duplicated:
            self.manager.transfer_account(self.account, self.manager.deleted_accounts, self.manager.active_accounts)
            self.manager.add_key(deleted_keys)
            self.show_message(self.SUCCESS_MESSAGES["data_restored"])
            raise NavigateTwoStepsBack
        self.show_message(self.ERROR_MESSAGES["exist"])
        return None
    

class DeleteAccountMenu(BaseMenu):
    """
    Handles deletion of a single account with user confirmation.

    This menu supports two deletion modes based on AccountState:
        - ACTIVE_ACCOUNTS: moves account to recycle bin (soft delete)
        - DELETED_ACCOUNTS: permanently removes account (hard delete)

    Responsibilities:
        - Prompt user for deletion confirmation
        - Execute appropriate delete strategy based on account state
        - Update account storage and unique key registry if needed
        - Provide success feedback after deletion
        - Navigate back after operation completion
    """
    OPTIONS = ("Confirm delete", "Cancel")
    SUCCESS_MESSAGES = {"account_deleted": "Account deleted!"}
    def __init__(self, account, manager, state):
        self.account = account
        self.manager = manager
        self.state = state
        if self.state == AccountState.ACTIVE_ACCOUNTS:
            self.prompts = {
                "delete_confirmation": """
                                Are you sure you want to delete this account?
                                (Deleted accounts moves to Recycle bin):
                                """
            }

        else:
            self.prompts = {
                "delete_confirmation": """
                            Are you sure you want to delete this service?
                            (THIS ACTION CAUSE DELETE SERVICE DATA FOREVER!):
                            """
            }

    def run(self) -> None:
        """
        Executes the account deletion workflow.

        Flow:
            - Displays a confirmation prompt based on account state
            - If user cancels, no action is performed
            - If confirmed:
                * ACTIVE_ACCOUNTS:
                    - Transfers account to recycle bin
                    - Removes account key from registry
                * DELETED_ACCOUNTS:
                    - Permanently deletes account data
            - Shows success message
            - Navigates two steps back in menu flow

        Returns:
            - None: If user cancels the operation.
        """
        confirmation = self.capture_menu_selection(self.OPTIONS,
                                                   self.prompts["delete_confirmation"],
                                                   allow_navigation_back=False)

        if confirmation == 1:
            if self.state == AccountState.ACTIVE_ACCOUNTS:
                account_keys = (self.account["service_name"], self.account["username"])
                self.manager.transfer_account(self.account, self.manager.active_accounts, self.manager.deleted_accounts)
                self.manager.remove_key(account_keys)
            else:
                self.manager.permanent_delete(self.account, self.manager.deleted_accounts)
            self.show_message(self.SUCCESS_MESSAGES["account_deleted"])
            raise NavigateTwoStepsBack
        return None


class DeleteAllAccountsMenu(BaseMenu):
    """
    Handles permanent deletion of all accounts in the recycle bin.

    This menu is responsible for:
        - Asking user for confirmation before destructive action
        - Permanently deleting all deleted accounts
        - Preventing accidental data loss through confirmation step
    """
    OPTIONS = ("Confirm delete", "Cancel")
    PROMPTS = {"delete_all_confirmation": """
                Are you sure you want to delete all services data?
                (THIS OPERATION CANNOT BE UNDONE!):
                """
               }
    def __init__(self, manager):
        self.manager = manager

    def run(self) -> None:
        """
        Executes the process of permanently deleting all deleted accounts.

        Flow:
            - Prompts the user for confirmation
            - If confirmed:
                * Permanently deletes all accounts in the recycle bin
            - If canceled:
                * No action is taken

        Returns:
            - None: Navigates back to the previous menu after deletion.
        """
        confirmation = self.capture_menu_selection(self.OPTIONS, self.PROMPTS["delete_all_confirmation"])
        if confirmation == 1:
            self.manager.permanent_delete_all(self.manager.deleted_accounts)
        return None

