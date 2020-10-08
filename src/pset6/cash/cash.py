from cs50 import get_float

QUARTER = 25
DIME = 10
NICKEL = 5
PENNY = 1

dollars = -1
while dollars < 0:
    dollars = get_float("Change owed: ")

penny = round(dollars, 2) * 100

quarter_count = int(round(penny / QUARTER, 2))
penny = penny - (quarter_count * QUARTER)

dime_count = int(round(penny / DIME, 2))
penny = penny - (dime_count * DIME)

nickel_count = int(round(penny / NICKEL, 2))
penny = penny - (nickel_count * NICKEL)

print(f"{int(penny + nickel_count + dime_count + quarter_count)}")