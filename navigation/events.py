"""
Implements navigation control signals for the menu system,
enabling structured transitions between application menus.
"""

class NavigateBack(Exception):
    """
    Raised to signal a request to return to the previous menu
    in the application's navigation stack.
    """
    pass