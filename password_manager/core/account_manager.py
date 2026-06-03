from ..utils import save_data


class AccountManager:
    """
        Manage user account lifecycles, validations, and data persistence.

        This class coordinates the business logic for creating, updating, and
        archiving account credentials. It ensures input compliance, guarantees
        data integrity via unique key tracking, and persists state changes.

    Attributes:
            active_accounts: Collections of currently active account credentials.
            deleted_accounts: Archive of removed account records.
            unique_keys: Unique composite identifiers to guarantee data integrity.
            CHARS_LIMIT: The maximum allowed length for validated text inputs.
    """
    CHARS_LIMIT = 30
    def __init__(self, active_accounts: list[dict], deleted_accounts: list[dict], unique_keys: set[tuple]):
        self.active_accounts = active_accounts
        self.deleted_accounts = deleted_accounts
        self.unique_keys = unique_keys

    def check_key(self, key: tuple) -> bool:
        """
        Check if a unique key already exists in the registered keys collection.

        Verifies the presence of the input tuple to prevent duplicate records
        from being saved in the system.

        Parameters:
            - key: The tuple containing unique field data to check.

        Returns:
            True if the key is a duplicate, False otherwise.
        """
        return key in self.unique_keys

    def length_validation(self, user_input: str) -> str:
        """
        Validate the length of the provided user input against system limits.

        Checks if the input string is completely empty or if its total length
        exceeds the maximum allowed character limit defined by the system.

        Parameters:
            - user_input: The string input entered by the user to be evaluated.

        Returns:
            - 'empty': if input is vacant
            - 'too_long': if input exceeds CHARS_LIMIT
            -'success': if input passes all length checks.
        """
        if not user_input:
            return "empty"
        if len(user_input) > self.CHARS_LIMIT:
            return "too_long"
        return "success"

    def create_accounts(self, service_name: str, username: str, password: str, key: tuple):
        """
        Create a new account entry, track its unique key, and persist the data.

        Appends the account details to the active accounts list, registers the
        associated unique key to prevent future duplicates, and commits the updated
        state to permanent storage.

        Parameters:
            service_name: The name of the platform or service.
            username: The identifier used for the account.
            password: The secret key for the account.
            key: The composite tuple used to uniquely identify this account record.
        """
        self.active_accounts.append(
            {"service_name": service_name,
             "username": username,
             "password": password
             })
        self.unique_keys.add(key)
        save_data(self.active_accounts, self.deleted_accounts)