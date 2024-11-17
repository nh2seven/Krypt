import string
import secrets
import random

def generate_password(length: int, include_letters: bool = True, 
                     include_digits: bool = True, 
                     include_symbols: bool = True) -> str:
    """Generate a secure random password."""
    # Original function remains unchanged
    ...

def generate_strong_password(length: int) -> str:
    """Generate a strong password with required character types.
    
    Args:
        length: Desired password length (minimum 8)
        
    Returns:
        Generated password string with at least one of each char type
    """
    # Ensure minimum length
    if length < 8:
        length = 8
        
    # Required characters
    required_chars = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice("!@#$%^&*()_+-=[]{}|;:,.<>?")
    ]
    
    # Character pool for remaining chars
    char_pool = (string.ascii_lowercase + 
                 string.ascii_uppercase + 
                 string.digits + 
                 "!@#$%^&*()_+-=[]{}|;:,.<>?")
    
    # Generate remaining characters
    remaining_length = length - len(required_chars)
    password_chars = required_chars + [secrets.choice(char_pool) 
                                     for _ in range(remaining_length)]
    
    # Shuffle password
    random.shuffle(password_chars)
    return ''.join(password_chars)

if __name__ == "__main__":
    exit("Invalid entry point")