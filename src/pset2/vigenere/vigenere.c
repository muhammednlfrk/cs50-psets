#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "../../../lib/cs50.h"

int isAlpha(char const *str);
int shift(char c);

int main(int argc, char const *argv[])
{
    // Check argument count
    if (argc < 2 || argc > 2 || !isAlpha(argv[1]))
    {
        printf("Usage: ./vigenere keyword\n");
        return 1;
    }

    // Plain text
    char *p = get_string("plaintext: ");

    // Secret key
    char const *ks = argv[1];
    int kslen = strlen(ks);
    int k[kslen];
    for (int i = 0; i < kslen; i++)
    {
        k[i] = shift(ks[i]);
    }

    // Secret key counter
    int ki = 0;

    // Cipher text
    char *c = p;

    // Chesar:
    for (int i = 0, n = strlen(p); i < n; i++)
    {
        if (ki >= kslen)
        {
            ki = 0;
        }

        if (isalpha(p[i]))
        {
            if (isupper(c[i]))
            {
                c[i] = ((p[i] + k[ki] - 65) % 26) + 65;
            }
            else
            {
                c[i] = ((p[i] + k[ki] - 97) % 26) + 97;
            }
            ki++;
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

int isAlpha(char const *str)
{
    for (int i = 0; i < strlen(str); i++)
    {
        if (!isalpha(str[i]))
        {
            return 0;
        }
    }

    return 1;
}

int shift(char c)
{
    if (isupper(c))
        return c - 65;
    else if (islower(c))
        return c - 97;
    return c;
}
