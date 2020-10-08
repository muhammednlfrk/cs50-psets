#include <stdio.h>

#include "../../../lib/cs50.h"

int main(void)
{
    int n;
    GET_HEIGHT:n = get_int("Height: ");

    if (n < 1 || n > 8)
    {
        goto GET_HEIGHT;
    }

    // printf("Stored: %i\n", n);

    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            if (n - i - j <= 1)
                printf("#");
            else
                printf(" ");
        }
        printf("  ");
        for (int j = 0; j < i + 1; j++)
        {
           printf("#");
        }
        printf("\n");
    }
}
