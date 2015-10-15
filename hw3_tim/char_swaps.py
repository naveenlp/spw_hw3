import random
from string import ascii_letters, digits, punctuation

def random_swap(char):
    pick = ascii_letters + digits + punctuation
    return random.choice(pick)

def char_to_num_swap(char):
    pick = digits
    return random.choice(pick)

def char_to_char_swap(char):
    pick = ascii_letters
    return random.choice(pick)

def to_cap_swap(char):
    return char.upper()

def vowel_swap(char):
    vowels = ['a','e','i','o','u','y']
    if char in vowels:
        char = random.choice(vowels)
    return char

def common_swaps(char):
    swapper = {"s": "$", "S": "$", "i": "!", "a": "@", "A": "4", "E": "&", "e": "&"}
    if char in swapper.keys():
        return swapper[char]
    else:
        return char
