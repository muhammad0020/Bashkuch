import pyperclip

def copy_to_clipboard(text: str) -> bool:
    """
    Copies text to system clipboard using pyperclip module.

    Parameters:
        - text: Text to copy to clipboard.

    Returns:
        - True: If copy operation was successful.
        - False: If copy operation failed.
    """
    try:
        pyperclip.copy(text)
        return True
    except pyperclip.PyperclipException:
        return False