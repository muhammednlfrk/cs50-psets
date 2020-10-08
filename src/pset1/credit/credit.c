#include <stdio.h>
#include <math.h>

#include "../../../lib/cs50.h"

typedef char byte;

const byte AMERICAN_EXPRESS = 34;
const byte AMERICAN_EXPRESS_2 = 37;
const byte AMERICAN_EXPRESS_LEN = 15;

const byte MASTER_CARD = 51;
const byte MASTER_CARD_2 = 52;
const byte MASTER_CARD_3 = 53;
const byte MASTER_CARD_4 = 54;
const byte MASTER_CARD_5 = 55;
const byte MASTER_CARD_LEN = 16;

const byte VISA = 4;
const byte VISA_CARD_LEN = 13;
const byte VISA_CARD_LEN_2 = 16;

const byte MAX_CARD_LEN = 16;
const byte MIN_CARD_LEN = 13;

byte get_digit_count(long l)
{
    int count = 1;
    while (l /= 10)
        count++;
    return count;
}

long get_digit(long l, long m)
{
    l %= m;
    if (m != 10)
    {
        m /= 10;
        l -= l % m;
    }
    return l != 0 ? (l > 9 ? l / m : l) : 0;
}

int main(void)
{
    // Get card information
    long credit_card_number = get_long("Number: ");
    byte credit_card_digit_count = get_digit_count(credit_card_number);

    if (credit_card_digit_count < MIN_CARD_LEN || credit_card_digit_count > MAX_CARD_LEN)
    {
        printf("INVALID\n");
        return 0;
    }

    long total = 0, grand_total = 0;
    long m = 10;
    byte double_coefficient = credit_card_digit_count % 2 == 0 ? 1 : 0;
    for (int i = credit_card_digit_count; i > 0; i--)
    {
        long digit = get_digit(credit_card_number, m);
        if ((i + double_coefficient) % 2 == 0)
        {
            long twice_of_digit = digit * 2;
            if (twice_of_digit < 10)
            {
                total += twice_of_digit;
            }
            else
            {
                byte twice_of_digit_count = get_digit_count(twice_of_digit);
                long todm = 10;
                for (int j = 0; j < twice_of_digit_count; j++)
                {
                    total += get_digit(twice_of_digit, todm);
                    todm *= 10;
                }
            }
        }
        else
        {
            grand_total += digit;
        }
        m *= 10;
    }
    grand_total += total;

    if (grand_total % 10 != 0)
    {
        printf("INVALID\n");
        return 0;
    }

    long lastdigit = get_digit(credit_card_number, pow(10, credit_card_digit_count));
    long last2digit = get_digit(credit_card_number, pow(10, credit_card_digit_count - 1)) + (10 * lastdigit);

    if (lastdigit == VISA && credit_card_digit_count >= VISA_CARD_LEN && credit_card_digit_count <= VISA_CARD_LEN_2)
        printf("VISA\n");
    else if ((last2digit == MASTER_CARD || last2digit == MASTER_CARD_2 || last2digit == MASTER_CARD_3 || last2digit == MASTER_CARD_4 || last2digit == MASTER_CARD_5) && credit_card_digit_count == MASTER_CARD_LEN)
        printf("MASTERCARD\n");
    else if ((last2digit == AMERICAN_EXPRESS || last2digit == AMERICAN_EXPRESS_2) && credit_card_digit_count == AMERICAN_EXPRESS_LEN)
        printf("AMEX\n");
    else
        printf("INVALID\n");
    return 0;
}