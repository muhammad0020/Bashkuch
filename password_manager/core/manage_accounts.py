"""
Account management: Handles account search, edit, and deletion operations.

Updates the unique_keys set and saves data after deletion.
"""

from .edit_accounts import edit_account

from ..common import  show_header, show_and_get
from ..common import  menu_titles, menu_options, messages

from ..utils import save_data
from ..utils import show_message, account_details, select_account


def manage_passwords(accounts_list, recycle_bin_data, unique_keys):
    """
    Interactive menu for searching, editing, and deleting vault accounts.

    Parameters:
        - accounts_list (list): List of saved accounts in vault list.
        - recycle_bin_data (list): List of deleted accounts in deleted_accounts list.
        - unique_keys (set): Set of unique service names and usernames to prevent save duplicated accounts.
    """

    def search_accounts() -> list:
        """
        Searches vault by service name and displays matching accounts.

        Returns:
            - List of matching account dictionaries. Empty list if no matches found.
        """
        print("=" * 46)
        service_name = input(messages["prompt"]["service_name"]).strip().lower()
        return [s for s in accounts_list if s["service_name"] == service_name]


    def delete_accounts():
        """
        Deletes selected account from vault (moves to deleted_accounts list).

        Returns:
            - Empty (str): If delete operation is successful and accounts_list is empty.
            - Success (str):
                * If delete operation is successful and accounts_list is not empty.
                * If user comes from search menu, delete operation is successful and search_data is not empty.
            - Search_results_deleted (str): If user comes from search section and deletes all services with same name.
            - Cancel (str): Users can backtrack to previous menus by selecting Cancel option.
        """

        index = item_index[-1]
        # ask user to confirm their decision
        confirmation = show_and_get(menu_options["manage"]["delete"], messages["prompt"]["delete_confirmation"])

        if confirmation == 1:  # confirm delete account
            # update unique_keys set
            unique_keys.discard((accounts_list[index]["service_name"], accounts_list[index]["username"]))
            recycle_bin_data.append(accounts_list.pop(index))  # add item to recycle bin
            save_data(accounts_list, recycle_bin_data)
            show_message(messages["success"]["deleted"])

            if not accounts_list:
                show_message(messages["error"]["no_password"])
                return "Empty"

            if search_data:  # if user comes from 'search services' menu
                # remove deleted account from search_data so doesn't show in search results and raise error
                search_data.remove(recycle_bin_data[-1])  # recent deleted account is last item in recycle_bin_data
                if not search_data:  # if after remove item list hasn't any item, means all search results deleted
                    return "Search_results_deleted"

                else:  # if items still exist in search_data, return Success cause return to show_saved_accounts()
                    return "Success"

            else:
                return "Success"

        else:
            return "Cancel"

    if not accounts_list:
        show_message(messages["error"]["no_password"])
        return

    show_header(menu_titles["manage"])
    search_data = []
    menu_stack = []
    item_index = []

    while True:
        if not menu_stack:
            choice = show_and_get(menu_options["manage"]["main"], messages["prompt"]["choice"])

            if choice == 1:
                menu_stack.append("search")

            elif choice == 2:
                menu_stack.append("select_accounts")

            else:
                break

        else:
            current_menu = menu_stack[-1]

            if current_menu == "search":
                result = search_accounts()

                if not result:
                    show_message(messages["error"]["not_found"])
                    menu_stack.pop()

                else:
                    choice = select_account(result)
                    if choice == "Back to previous menu":
                        menu_stack.pop()
                    else:
                        # choose from search results. need convert to exact index in original list
                        item_index.append(accounts_list.index(result[choice]))
                        menu_stack.append("show_details")

            elif current_menu == "select_accounts":
                item_index.clear()  # delete previous item indexes to prevent infinite re-entry
                choice = select_account(accounts_list)
                if choice == "Back to previous menu":
                    # Prevent infinite loop by skipping to parent menu when previous menu was 'search_password'
                    if len(menu_stack) >= 2 and menu_stack[-2] == "search":
                        del menu_stack[-2:]
                        # Clear temporary search results from display list after service display completes
                        search_data.clear()

                    else:
                        menu_stack.pop()

                else:
                    menu_stack.append("show_details")
                    item_index.append(choice)

            elif current_menu == "show_details":
                choice = account_details(accounts_list[item_index[-1]], menu_options["manage"]["saved_accounts"])

                if choice == 1:
                    menu_stack.append("edit")

                elif choice == 2:
                    menu_stack.append("delete")

                else:
                    menu_stack.pop()

            elif current_menu == "edit":
                edit_account(accounts_list, item_index[-1], unique_keys, recycle_bin_data)
                menu_stack.pop()

            elif current_menu == "delete":
                choice = delete_accounts()
                if choice == "Empty":
                    break  # there is nothing to show. exit to main file

                elif choice == "Success":
                    # removing data removes account from accounts_list. so back to show_saved_accounts()
                    del menu_stack[-2:]

                elif choice == "Search_results_deleted":
                    # all searched accounts have been deleted, there is no service in search_data to show
                    del menu_stack[-4:]  # back to manage_passwords main menu

                elif choice == "Cancel":
                    menu_stack.pop()
