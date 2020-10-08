from sys import argv
from cs50 import get_string

argc = len(argv)

def main():
    if argc != 2 or argv[1].isdigit() == False:
        print("Usage: python3 caesar.py key")
        return 1
    
    k = int(argv[1])
    p = get_string("plaintext: ")
    p_len = len(p)
    c = ""

    for i in range(p_len):
        if p[i].isalpha():
            if p[i].isupper():
                c = c + chr(((ord(p[i]) + k - 65) % 26) + 65)
            else:
                c = c + chr(((ord(p[i]) + k - 97) % 26) + 97)
        else:
            c = c + p[i]
            pass
        pass

    print(f"ciphertext: {c}")
    return 0

if __name__ == "__main__":
    exit(main())
    pass