from cs50 import get_string
from sys import argv

# Get argument count
argc = len(argv)

# Initialization point of program
def main() -> int:
    # Check arguments
    if argc != 2:
        print("Usage: python3 bleep.py [dictionary]")
        return 1

    # Get message
    message = get_string("What message would you like to censor?\n")

    # Get file path
    dictinary_file_path = argv[1]

    # Open dictipnary file
    dictionary_file = open(dictinary_file_path)

    # Get banned words set
    dictionary = set(x for x in dictionary_file.readlines())

    # Clese dictionary file
    dictionary_file.close()

    # Define result string
    result = ""

    # Replace banned words
    for word in message.split(" "):
        if word.lower() + "\n" in dictionary:
            result = result + ("*" * len(word)) + " "
        else:
            result = result + word + " "

    # Print result
    print(result)

    # Return success result
    return 0

# Initialize the program
if __name__ == "__main__":
    exit(main())
