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


class NavigateTwoStepsBack(Exception):
    """
    Custom control-flow exception used to navigate two steps back
    in the menu stack.

    This exception is raised when a deep navigation rollback is required,
    allowing the application to exit multiple nested menu levels without
    tightly coupling UI components.
    """
    pass