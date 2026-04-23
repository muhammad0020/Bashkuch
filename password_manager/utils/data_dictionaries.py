"""
Standard dictionaries for menu system:

- `menu_titles`: Dictionary of menu title strings
- `menu_options`: Dictionary of option labels and their actions
- `messages`: Nested dictionary with keys:
    * `success`: Success messages
    * `error`: Error messages
    * `prompt`: User prompts
"""

menu_titles = {
    "main": "PASSWORD MANAGER",
    "add": "ADD PASSWORD",
    "manage": "MANAGE PASSWORDS",
    "generate": "GENERATE PASSWORDS",
    "recycle": "RECYCLE BIN"
}

menu_options = {
    "main": {
        "main": ("Add password", "Manage passwords", "Generate password", "Recycle bin", "Exit"),
        "exit": ("Cancel", "Exit program")
    },
    "manage": {
        "main": ("Search services", "Show saved accounts", "Back to menu"),
        "saved_accounts": ("Edit information", "Delete service", "Choose another account"),
        "search": ("Edit information", "Delete service", "Search another account"),
        "edit": ("Edit service name", "Edit username", "Edit password", "Edit all"),
        "delete": ("Confirm delete", "Cancel")
    },
    "generate": {
        "main": ("Generate another password", "Copy password to clipboard", "Exit to main menu"),
        "after_copy": ("Generate another password", "Exit to main menu")
    },
    "recycle": {
        "main": ("Show deleted accounts", "Empty recycle bin", "Back to menu"),
        "second": ("Restore", "Delete", "Choose another account"),
        "delete": ("Confirm delete", "Cancel")
    }
}

messages = {
    "success": {
        "key": "key generated",
        "saved": "Password saved!",
        "deleted": "Service deleted!",
        "restored": "Data restored!",
        "emptied": "Recycle bin emptied!",
        "copied": "Password copied to clipboard!",
        "service_updated": "Service name updated!",
        "username_updated": "Username updated!",
        "password_updated": "Password updated!",
        "information_updated": "Information updated!"
    },

    "error": {
        "empty_service_field": "Service name cannot be empty!",
        "empty_username_field": "Username cannot be empty!",
        "empty_password_field": "Password field cannot be empty!",
        "no_password": "No password saved!",
        "not_found": "This service does not exist!",
        "bin_empty": "Recycle bin is empty!",
        "not_copied": "Clipboard doesn't work",
        "invalid": "Invalid input",
        "exist": "This service with this username is already exist"
    },

    "prompt": {
        "service_name": "Enter service name: ",
        "new_service": "Enter new service name: ",
        "username": "Enter username: ",
        "new_username": "Enter new username: ",
        "password": "Enter password: ",
        "new_password": "Enter new password: ",
        "choice": "Choose an option: ",
        "choose_service": "Choose a service: ",

        "delete_confirmation": """
                Are you sure you want to delete this service?
                (Deleted items moves to Recycle bin):
                """,

        "delete_last_confirmation": """
                Are you sure you want to delete this service?
                (THIS ACTION CAUSE DELETE SERVICE DATA FOREVER!):
                """,

        "remove_all_confirmation": """
                Are you sure you want to delete all services data?
                (THIS OPERATION CANNOT BE UNDONE!):
                """,

        "exit": "Are you sure you want to exit?:"
    }
}
