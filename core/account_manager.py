from .storage import save_data

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

    def add_key(self, account_key: tuple[str, str]):
        """
        Adds an account key to the unique keys set.

        The key is used to track existing accounts and prevent
        duplicate service name and username combinations.

        Parameters:
            - key: A tuple in the format (service_name, username).
        """
        self.unique_keys.add(account_key)

    def remove_key(self, account_key: tuple[str, str]):
        """
        Removes an account key from the unique keys set.

        Parameters:
            account_key: A tuple in the format
                (service_name, username).
        """
        self.unique_keys.discard(account_key)

    def check_key(self, key: tuple[str, str]) -> bool:
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

    def edit_account(self, account: dict, new_data: str, key:str, *, unique_key_update: bool=True):
        """
        Updates a specific field of an account and manages unique constraints.

        Modifies the provided account dictionary with the new data. If unique_key_update
        is enabled, it dynamically extracts the composite keys, updates the internal
        uniqueness tracking set to prevent duplication, and then commits the changes
        to the persistent storage.

        Parameters:
            account: The target account record to be modified.
            new_data: The new value to assign to the target field.
            key: The exact dictionary key to be updated.
            unique_key_update (optional): Determines whether to recalculate
                and refresh the composite unique keys cache. Defaults to True.

        Side Effects:
            - Modifies the state of `self.unique_keys` if unique_key_update is True.
            - Invokes `save_data` to write the updated lists to disk.
        """
        if unique_key_update:
            account_keys = list(account.keys())
            old_unique_keys = (account[account_keys[0]], account[account_keys[1]])
            self.unique_keys.discard(old_unique_keys)
            account[key] = new_data
            new_unique_keys = (account[account_keys[0]], account[account_keys[1]])
            self.unique_keys.add(new_unique_keys)
        else:
            account[key] = new_data
        save_data(self.active_accounts, self.deleted_accounts)

    def search_accounts(self, service_name: str) -> list:
        """
        Search stored accounts by service name.

        Parameters:
            - service_name:
                Name of the service to search for.

        Returns:
            - List of matching account dictionaries.
              Returns an empty list if no matching accounts are found.
        """
        return [account for account in self.active_accounts if account["service_name"] == service_name]

    def transfer_account(self, account: dict, source: list[dict], destination: list[dict]):
        """
        Transfers an account from one account list to another.

        The account is added to the destination list, removed from
        the source list, and the updated data is saved.

        Parameters:
            - account: The account dictionary to transfer.
            - source: The list currently containing the account.
            - destination: The list that will receive the account.
        """
        destination.append(account)
        source.remove(account)
        save_data(self.active_accounts, self.deleted_accounts)

    def permanent_delete(self, account: dict, source: list[dict]):
        """
        Permanently removes an account from the specified list.

        The account is deleted from the source list and the updated
        data is saved to storage.

        Parameters:
            - account: The account dictionary to delete.
            - source: The list containing the account to be removed.
        """
        source.remove(account)
        save_data(self.active_accounts, self.deleted_accounts)

    def permanent_delete_all(self, source: list[dict]):
        """
        Permanently removes all accounts from the specified list.

        The source list is cleared and the updated data is saved
        to storage.

        Parameters:
            - source: The account list to clear.
        """
        source.clear()
        save_data(self.active_accounts, self.deleted_accounts)
