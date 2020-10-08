from sys import argv
from cs50 import get_string

# Get argument count
argc = int(len(argv))

# Initialization point of program
def main() -> int:
    # Check arguments
    if argc != 2 or argv[1].isalpha() == False:
        print("Usage: python3 vigenere.py key")
        return 1
    
    # Get key
    key = argv[1]
    key_len = len(key)

    # Shift all key chars
    key = shiftall(key)

    # Get plaintext
    plaintext = get_string("plaintext: ")

    # Define ciphertext string
    ciphertext = ""

    # Define key counter
    key_counter = 0
    
    # Encrypt plaintext
    for i in range(len(plaintext)):
        if key_counter >= key_len:
            key_counter = 0
            pass
        if plaintext[i].isalpha():
            if plaintext[i].isupper():
                ciphertext = ciphertext + chr(((ord(plaintext[i]) + ord(key[key_counter]) - 65) % 26) + 65)
            else:
                ciphertext = ciphertext + chr(((ord(plaintext[i]) + ord(key[key_counter]) - 97) % 26) + 97)
            key_counter = key_counter + 1
        else:
            ciphertext = ciphertext + plaintext[i]

    # Print the ciphertext
    print(f"ciphertext: {ciphertext}")   

    # Return success result
    return 0

def shiftall(s) -> str:
    r = ""
    for i in range(len(s)):
        if s[i].isupper():
            r = r + chr(ord(s[i]) - 65)
        elif s[i].islower():
            r = r + chr(ord(s[i]) - 97)
    return r

# Call main function
if __name__ == "__main__":
    exit(main())