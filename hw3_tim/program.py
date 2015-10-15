import sys
import random
import char_swaps
import noise

def main(argv):
    input_password = argv[1]
    print perform_swaps(input_password, getattr(char_swaps,"common_swaps"), 1, 4)

    print generate_honey(argv[1])


def generate_honey(password, seeders=None):
    """
    Desc:
        Generates honeywords from an original password

    Args:
        password : the true password
        seeders  : list of passwords from which to seed fake ones

    Returns:
        List of 10 passwords. 9 of which are fake and the original
    """
    original = password


    swap_funcs = [method for method in dir(char_swaps) if callable(getattr(char_swaps, method))]
    noise_funcs = [method for method in dir(noise) if callable(getattr(noise, method))]

    honey = [perform_swaps(password, getattr(char_swaps,random.choice(swap_funcs)), 0, len(password)) for i in range(0,9)]
    honey.insert(random.randint(0,len(honey)), original)

    return set(honey)


def perform_swaps(string, swap_func, first, last=None):
    """
    Desc:
        Performs a swap on a range of a string

    Args:
        string    : an arbitraty string
        swap_func : function to be applied on the range of the string
        first     : first element of the range
        last      : last element of the range (optional)

    Returns:
        String with the appropriate swaps
    """

    if last is None:
        last = first + 1

    swapped = ''.join(list(string[0:first]) + map(swap_func, string[first:last]) + list(string[last:]))

    return swapped


if __name__ == "__main__":
    main(sys.argv)
