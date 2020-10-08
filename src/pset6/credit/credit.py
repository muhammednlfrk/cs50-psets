from cs50 import get_int

AMERICAN_EXPRESS = 34
AMERICAN_EXPRESS_2 = 37
AMERICAN_EXPRESS_LEN = 15
MASTER_CARD = 51
MASTER_CARD_2 = 52
MASTER_CARD_3 = 53
MASTER_CARD_4 = 54
MASTER_CARD_5 = 55
MASTER_CARD_LEN = 16
VISA = 4
VISA_CARD_LEN = 13
VISA_CARD_LEN_2 = 16
MAX_CARD_LEN = 16
MIN_CARD_LEN = 13


def main():
    # Get arguments
    card_number = get_int("Number: ")
    card_number_str = str(card_number)
    card_number_str_len = len(card_number_str)

    # Check length
    if card_number_str_len < MIN_CARD_LEN and card_number_str_len > MAX_CARD_LEN:
        print("INVALID")
        return 1

    # Holds the total value
    total = 0

    # Multiply all digits by 2, starting from the second last digit,
    # and add the digits of the resulting numbers
    for i in range(card_number_str_len - 2, -1, -2):
        digit = int(card_number_str[i])
        twice_of_digit = digit * 2
        twice_of_digit_str = str(twice_of_digit)
        twice_of_digit_str_len = len(twice_of_digit_str)
        for j in range(twice_of_digit_str_len):
            twice_of_digit_digit = int(twice_of_digit_str[j])
            total = total + twice_of_digit_digit

    # Scroll the numbers not multiplied by two
    for i in range(card_number_str_len - 1, -1, -2):
        digit = int(card_number_str[i])
        total = total + digit

    # Get total str
    total_str = str(total)

    # Return 'INVALID' if the last digit of the total is not equal '0'
    if total_str[-1:] != '0':
        print("INVALID")
        return 1

    # Get tast digits
    first_digit = int(card_number_str[0:1])
    first_two_digit = int(card_number_str[0:2])

    # Check card types
    if first_digit == VISA and card_number_str_len >= VISA_CARD_LEN and card_number_str_len <= VISA_CARD_LEN_2:
        print("VISA")
    elif (first_two_digit == MASTER_CARD or first_two_digit == MASTER_CARD_2 or first_two_digit == MASTER_CARD_3 or first_two_digit == MASTER_CARD_4 or first_two_digit == MASTER_CARD_5) and card_number_str_len == MASTER_CARD_LEN:
        print("MASTERCARD")
    elif (first_two_digit == AMERICAN_EXPRESS or first_two_digit == AMERICAN_EXPRESS_2) and card_number_str_len == AMERICAN_EXPRESS_LEN:
        print("AMEX")
    else:
        print("INVALID")

    # End of main function
    return 0

# Call the main function
if __name__ == "__main__":
    main()
    pass