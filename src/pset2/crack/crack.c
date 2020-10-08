// Includes:
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <crypt.h>

void checkpasswordhashs(char *passwordhash, char *buffer, int bufferlen, const int charslen, int len, char *salt);

// Maximum length of possible passwords.
const int MAX_LEN = 5;

// String of characters contained in possible passwords
const char *CHARS = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz";

// If password is detected are equal 1 else are equal 0.
int passwordisdetected = 0;

// Initialization point of program.
int main(int argc, char const *argv[])
{
    // If argument count is invalid.
    if (argc > 2 || argc < 2)
    {
        printf("Invalid arguments\nUsage: ./crack [password-bufferhash]\n");
        return 1;
    }

    // Gets password salt.
    char *salt = (char *)malloc(2 * sizeof(char));
    *(salt + 0) = argv[1][0];
    *(salt + 1) = argv[1][1];

    // Gets password hash.
    char *passwordhash = (char *)argv[1];

    // Gets chars length.
    int charslen = strlen(CHARS);

    // For GUI.
    printf("\n");

    // Check passwords.
    for (int i = 1; i <= MAX_LEN; i++)
    {
        // Checks the password of length i.
        checkpasswordhashs(passwordhash, (char *)malloc(1 * sizeof(char)), 1, charslen, i, salt);

        // Brokes the loop, if password detected.
        if (passwordisdetected)
        {
            passwordisdetected = 0;
            break;
        }
    }
}

// Adds c in the str pointer. Returns string length.
int addstr(char *str, int slen, char c)
{
    // If the str size is enough adds c in str and returns slen.
    if (*(str + slen - 1) == '\000')
    {
        *(str + slen - 1) = c;
        return slen;
    }
    // If the str size is not enough resizes str, adds c in str and returns (slen + 1).
    else
    {
        str = (char *)realloc(str, (slen + 1) * sizeof(char));
        *(str + slen) = c;
        return (slen + 1);
    }
}

// Retrieves a substring from *str. The substring starts point at *(str + index) and ends point at *(str + index + i).
char *substr(char *str, int index, int length)
{
    // Returns empty string if substring is empty.
    if (length < 1)
    {
        return (char *)malloc(1 * sizeof(char));
    }

    // Creates substring pointer.
    char *substr = (char *)malloc(length * sizeof(char));

    // Adds the string characters into the substring.
    for (int i = 0; i < length; i++)
    {
        *(substr + i) = *(str + index + i);
    }

    // Returns generated substring.
    return substr;
}

// Checks if s1 and s2 are equal.
int equalsstr(char *s1, char *s2)
{
    // Gets length of strings.
    int s1l = strlen(s1), s2l = strlen(s2);

    // Checks lenghts of strings.
    if (s1l != s2l)
    {
        return 0;
    }

    // Checks chars of s1 and s2 are equal.
    for (int i = 0; i < s1l; i++)
    {
        if (*(s1 + i) != *(s2 + i))
        {
            return 0;
        }
    }

    // Return equals return.
    return 1;
}

// Checks password hash.
void checkpasswordhashs(char *passwordhash, char *buffer, int bufferlen, const int charslen, int len, char *salt)
{
    // Password is detected break the loop.
    if (passwordisdetected)
    {
        return;
    }

    // Generates and tries possible password combinations.
    for (int i = 0; i < charslen; i++)
    {
        // Adds char in buffer.
        bufferlen = addstr(buffer, bufferlen, *(CHARS + i));

        // Adds chars if character length is not achieved.
        if (len > 1)
        {
            checkpasswordhashs(passwordhash, buffer, bufferlen, charslen, len - 1, salt);
        }
        // Else checks the password
        else
        {
            // Creates hash of the password.
            char *bufferhash = crypt(buffer, salt);

            // Prints the password and hash the terminal.
            printf("\033[A\33[2KT\rTrying %s, hash: %s\n", buffer, bufferhash);

            // Checks the password, if password is correct braks the loop.
            if (equalsstr(passwordhash, bufferhash))
            {
                passwordisdetected = 1;
                printf("Password is %s\n", buffer);
                break;
            }
        }

        // Removes last char of buffer.
        buffer = substr(buffer, 0, bufferlen - 1);

        // Updates buffer length.
        if (bufferlen > 1)
        {
            bufferlen--;
        }
    }
}
