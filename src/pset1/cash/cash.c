#include <stdio.h>
#include <math.h>

#include "../../../lib/cs50.h"

const int QUARTER = 25;
const int DIME = 10;
const int NICKEL = 5;
const int PENNY = 1;

int main(void)
{
    float dollars;

GET_CHANGE:
    dollars = get_float("Change owed: ");

    if (dollars < 0)
        goto GET_CHANGE;

    int penny = round(dollars * 100);
    printf("penny: %i\n", penny);

    printf("\n");
    int querter_countf = round(penny / QUARTER);
    penny -= querter_countf * QUARTER;
    printf("querter_countf: %i\n", querter_countf);
    printf("penny: %i\n", penny);

    printf("\n");
    int dime_countf = round(penny / DIME);
    penny -= dime_countf * DIME;
    printf("dime_countf: %i\n", dime_countf);
    printf("penny: %i\n", penny);

    printf("\n");
    int nickel_countf = round(penny / NICKEL);
    penny -= nickel_countf * NICKEL;
    printf("nickel_countf: %i\n", nickel_countf);
    printf("penny: %i\n", penny);

    printf("\n");
    int penny_countf = penny;

    printf("%i\n", querter_countf + dime_countf + nickel_countf + penny_countf);
}
