#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "../../../lib/cs50.h"

int isNumber(char const *str);

int main(int argc, char const *argv[])
{
    // Check argument count
    if (argc != 2|| !isNumber(argv[1]))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // Plain text
    char *p = get_string("plaintext: ");

    // Secret key
    char *tendptr;
    long k = strtol(argv[1], &tendptr, 10);

    // Cipher text
    char *c = p;

    // Chesar:
    for (int i = 0, n = strlen(p); i < n; i++)
    {
        if (isalpha(p[i]))
        {
            // Encrypts uppercase letters.
            if (isupper(c[i]))
            {
                c[i] = ((p[i] + k - 65) % 26) + 65;
            }

            // Encrypts lowercase letters
            else
            {
                c[i] = ((p[i] + k - 97) % 26) + 97;
            }
        }
        else
        {
            c[i] = p[i];
        }
    }

    // Print cipher text
    printf("ciphertext: %s\n", c);

    // Return success result
    return 0;
}

int isNumber(char const *str)
{
    for (int i = 0; i < strlen(str); i++)
    {
        if (!isdigit(str[i]))
        {
            return 0;
        }
    }

    return 1;
}
