from nltk.tokenize import sent_tokenize
import sys

# Return lines in both a and b
def lines(a, b):
    # Get lines of files
    a_lines = a.split("\n")
    b_lines = b.split("\n")

    # Get equal lines
    equal_lines = [x for x in a_lines for y in b_lines if x == y]

    # Return equal lines
    return set(equal_lines)

# Return sentences in both a and b
def sentences(a, b):
    # Get sentences of a and b
    a_sentences = sent_tokenize(a)
    b_sentences = sent_tokenize(b)

    # Get equal sentences
    equal_sentences = [x for x in a_sentences for y in b_sentences if x == y]

    # Return eqaul lines
    return set(equal_sentences)

# Return substrings of length n in both a and b
def substrings(a, b, n):
    # Get words
    a_words = get_words(a)
    b_words = get_words(b)

    # Get substrings
    a_substrings = get_substrings(a_words, n)
    b_substrings = get_substrings(b_words, n)

    # Get equal substrings
    equal_substrings = [x for x in a_substrings for y in b_substrings if x == y]

    # Return substrings
    return set(equal_substrings)

# Gets substrings of s of n lengths
def get_substrings(words, n):
    # Create substrings list
    substrs = set()

    # Get substrings
    for word in words:
        word_len = len(word)
        end_index = n
        for i in range(word_len):
            if end_index <= word_len:
                substrs.add(word[i:end_index])
            else:
                break
            end_index = i + n + 1

    # Return substrings
    return substrs

# Gets words in the s str
def get_words(s):
    # Get alphanumeric s
    alnum_s = ""
    for c in s:
        if c.isalnum() or c == " ":
            alnum_s += c
        else:
            alnum_s += " "
    
    # Split words and return
    return [word for word in alnum_s.split(" ") if word != ""]