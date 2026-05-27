"""
Secure deletion management: handles restore and permanent deletion with duplicate prevention.

Prevents restoring duplicated accounts to maintain data integrity.

Saves data after each operation.
"""

from ..common import show_header, show_and_get
from ..common import menu_titles, menu_options, messages
from ..utils import select_account, show_message, account_details
from ..utils import save_data


def recycle_bin(accounts_list, recycle_bin_data, unique_keys):
    """
    Manages deleted accounts. Supports restore or permanent delete operations.

    Parameters:
        - accounts_list (list): List of saved accounts in vault list.
        - recycle_bin_data (list, dict): List of deleted accounts in deleted_accounts list.
        - unique_keys (set): Set of unique service names and usernames to prevent save duplicated accounts.
    """

    def restore():
        """
        Restores deleted account to vault end if not already present.
        Prevents duplicates by comparing decrypted service_name + username with unique keys.

        Returns:
            - Empty (str): If restore operation is successful and recycle bin is empty.
            - Success (str): If restore operation is successful and recycle bin is not empty.
            - Back to previous menu (str): If selected data already exists in vault list.
        """

        list_index = item_index[-1] # obtain service index that saved to list earlier
        deleted_keys = (recycle_bin_data[list_index]["service_name"], recycle_bin_data[list_index]["username"])

        if not deleted_keys in unique_keys:
            accounts_list.append(recycle_bin_data.pop(list_index))
            unique_keys.add((accounts_list[-1]["service_name"], accounts_list[-1]["username"]))
            save_data(accounts_list, recycle_bin_data)
            show_message(messages["success"]["restored"])

            if not recycle_bin_data:
                show_message(messages["error"]["bin_empty"])
                return "Empty"

            else:
                return "Success"

        else:
            show_message(messages["error"]["exist"])
            return "Back to previous menu"


    def delete():
        """
        Delete selected account from deleted_accounts list.

        Returns:
            - Empty (str): If delete operation is successful and recycle bin is empty.
            - Success (str): If delete operation is successful and recycle bin is not empty.
            - Cancel (str): Users can backtrack to previous menus by selecting Cancel option.
        """

        list_index = item_index[-1]  # obtain service index that saved to list earlier
        decision = show_and_get(menu_options["recycle"]["delete"], messages["prompt"]["delete_last_confirmation"])
        if decision == 1:
            recycle_bin_data.pop(list_index)
            show_message(messages["success"]["deleted"])

            if not recycle_bin_data:
                show_message(messages["error"]["bin_empty"])
                return "Empty"

            else:
                return "Success"

        else:
            return "Cancel"


    def remove_all():
        """
        Removes all deleted accounts in recycle_bin_data.

        Returns:
            - Exit (str): If all services have been removed successfully.
            - Back to previous menu (str): If user select 'Back to previous menu' option.
        """

        decision = show_and_get(menu_options["recycle"]["delete"], messages["prompt"]["remove_all_confirmation"])

        if decision == 1:
            recycle_bin_data.clear()
            save_data(accounts_list, recycle_bin_data)
            show_message(messages["success"]["emptied"])
            return "Exit"

        else:
            return "Back to previous menu"


    # check deleted_accounts list not empty
    if not recycle_bin_data:
        show_message(messages["error"]["bin_empty"])
        return

    show_header(menu_titles["recycle"])
    menu_stack = []
    item_index = []

    while True:
        if not menu_stack:
            choice = show_and_get(menu_options["recycle"]["main"], messages["prompt"]["choice"])
            if choice == 1:
                menu_stack.append("show_accounts")

            elif choice == 2:
                menu_stack.append("remove_all")

            elif choice == 3:
                break

        else:
            current_menu = menu_stack[-1]

            if current_menu == "show_accounts":
                item_index.clear()  # delete previous item indexes to prevent infinite re-entry
                choice = select_account(recycle_bin_data)
                if choice == "Back to previous menu":
                    menu_stack.pop()

                else:
                    menu_stack.append("show_details")
                    item_index.append(choice)

            elif current_menu == "show_details":
                choice = account_details(recycle_bin_data[item_index[-1]], menu_options["recycle"]["second"])
                if choice == 1:
                    menu_stack.append("restore")

                elif choice == 2:
                    menu_stack.append("delete")

                elif choice == 3:
                    menu_stack.pop()

            elif current_menu == "restore":
                choice = restore()
                if choice == "Success":
                    # restoring data removes account from deleted_accounts list. so back to show_deleted_accounts()
                    del menu_stack[-2:]

                elif choice == "Empty":
                    # there is nothing to show. exit to main file
                    break

                elif choice == "Back to previous menu":
                    # selected item is already exist in vault. back to
                    menu_stack.pop()

            elif current_menu == "delete":
                choice = delete()
                if choice == "Success":
                    # removing data removes account from deleted_accounts list. so back to show_deleted_accounts()
                    del menu_stack[-2:]

                elif choice == "Empty":
                    # there is nothing to show. exit to main file
                    break

                else:
                    menu_stack.pop()

            elif current_menu == "remove_all":
                choice = remove_all()
                if choice == "Back to previous menu":
                    menu_stack.pop()

                else:
                    # there is nothing to show. exit to main file
                    break
