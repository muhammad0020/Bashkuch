"""
Provides password generation and validation utilities.

Includes functionality for generating cryptographically secure passwords
containing a mix of character categories, as well as validation of
user-supplied password length values.
"""

import string
import secrets


def length_validation(length: str, min_length: int, max_length: int) -> bool:
    """
    Validate a password length provided as a string.

    Parameters:
        - length: User-supplied password length to validate.
        - min_length: Minimum allowed password length.
        - max_length: Maximum allowed password length.

    Returns:
         - True if the value contains only decimal digits and falls
           within the configured password length range; otherwise returns False.
    """
    return len(length) < 3 and length.isdecimal() and min_length <= int(length) <= max_length


def generate_secure_password(length: int=8) -> str:
    """
    Generate a cryptographically secure random password.

    The generated password is guaranteed to contain at least one uppercase
    letter, one lowercase letter, one digit, and one punctuation character.
    The remaining characters are selected from the full character set and
    the final password is securely shuffled before being returned.

    Parameters:
        - length: Desired password length.

    Returns:
        - A randomly generated secure password.
    """
    # Ensure generated password has all character types
    generated_password = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.digits),
        secrets.choice(string.punctuation)
    ]

    all_chars = string.ascii_letters + string.digits + string.punctuation
    generated_password += [secrets.choice(all_chars) for _ in range(length - 4)]
    secret_system = secrets.SystemRandom()
    secret_system.shuffle(generated_password)
    return "".join(generated_password)