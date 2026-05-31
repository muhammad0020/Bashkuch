"""
Account management: Handles account search, edit, and deletion operations.

Updates the unique_keys set and saves data after deletion.
"""

from .edit_accounts import edit_account

from ..common import  BaseMenu
from ..common import  menu_titles, menu_options, messages

from ..utils import delete_accounts, select_account, account_details


def manage_passwords(accounts_list, recycle_bin_data, unique_keys):
    """
    Interactive menu for searching, editing, and deleting vault accounts.

    Parameters:
        - accounts_list (list): List of saved accounts in vault list.
        - recycle_bin_data (list): List of deleted accounts in deleted_accounts list.
        - unique_keys (set): Set of unique service names and usernames to prevent save duplicated accounts.
    """
    account_manager = BaseMenu()
    def search_accounts() -> list:
        """
        Searches vault by service name and displays matching accounts.

        Returns:
            - List of matching account dictionaries. Empty list if no matches found.
        """
        print("=" * 46)
        service_name = input(messages["prompt"]["service_name"]).strip().lower()
        return [s for s in accounts_list if s["service_name"] == service_name]


    if not accounts_list:
        account_manager.show_message(messages["error"]["no_password"])
        return

    account_manager.show_header(menu_titles["manage"])
    menu_stack = []
    item_index = None
    search_results = None

    while True:
        if not menu_stack:
            choice = BaseMenu.get_and_validate(menu_options["manage"]["main"], messages["prompt"]["choice"])

            if choice == 1:
                menu_stack.append("search")

            elif choice == 2:
                menu_stack.append("select_accounts")

            else:
                break

        else:
            current_menu = menu_stack[-1]

            if current_menu == "search":
                search_results = search_accounts()

                if not search_results:
                    BaseMenu.show_message(messages["error"]["not_found"])
                    menu_stack.pop()

                else:
                    menu_stack.append("select_accounts")

            elif current_menu == "select_accounts":
                # Show search results if available (user came from search menu); otherwise display all saved accounts.
                if search_results:  # If user comes from search menu, search_results isn't 'None'
                    choice = select_account(search_results)
                    # 'Back to previous menu' option should not be treated as an account index.
                    # Ensure user choice is not a string to avoid TypeError when used as index.
                    if isinstance(choice, int):
                        choice = accounts_list.index(search_results[choice])
                else:
                    choice = select_account(accounts_list)
                if choice == "Back to previous menu":
                    # Prevent infinite loop by skipping to parent menu when previous menu was 'search_password'
                    if search_results:
                        del menu_stack[-2:]
                        # Clear temporary search results from display list after service display completes
                        search_results.clear()

                    else:
                        menu_stack.pop()

                else:
                    menu_stack.append("show_details")
                    item_index = choice

            elif current_menu == "show_details":
                choice = account_details(accounts_list[item_index], menu_options["manage"]["saved_accounts"])

                if choice == 1:
                    menu_stack.append("edit")

                elif choice == 2:
                    menu_stack.append("delete")

                else:
                    menu_stack.pop()

            elif current_menu == "edit":
                edit_account(accounts_list, item_index, unique_keys, recycle_bin_data)
                menu_stack.pop()

            elif current_menu == "delete":
                if search_results:  # if user comes from 'search services' menu search_result isn't 'None'
                    choice = delete_accounts(accounts_list, recycle_bin_data, item_index, unique_keys)
                    # After removing an account from accounts list, it should no longer appear in search results.
                    # Any attempt to access it should raise an error.
                    search_results.remove(recycle_bin_data[-1])  # recent deleted account is last item in recycle_bin_data
                    if choice == "Empty":
                        break  # All saved accounts have been deleted; return to main_menu.py.

                    # No search results left; return to the main menu of manage_accounts.py.
                    elif not search_results:
                        del menu_stack[-2:]

                else:
                    choice = delete_accounts(accounts_list, recycle_bin_data, item_index, unique_keys)
                    if choice == "Empty":
                        break  # There is nothing to show. exit to main_menu.py

                if choice == "Success":
                    # removing data removes account from accounts_list. so back to show_saved_accounts()
                    del menu_stack[-2:]

                elif choice == "Cancel":
                    menu_stack.pop()
