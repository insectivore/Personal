import random

def create_ascii_range_string(start: int, stop: int):
    string = ""
    for x in range(start, stop):
        letter = chr(x)
        string += letter
    return string

def create_uppercase_letters_string():
    caprange = create_ascii_range_string(65, 91)
    return caprange

def create_lowercase_letters_string():
    lowrange = create_ascii_range_string(97, 123)
    return lowrange

def create_digits_string():
    digrange = create_ascii_range_string(48, 58)
    return digrange

def create_symbols_string():
    symrange = create_ascii_range_string(33, 48)
    return symrange

def get_random_char_from_string(string):
    length = len(string)
    min = 0
    max = length - 1
    num = random.randint(min, max)
    random_char = string[num]
    return random_char

def generate_random_password(numUp, numLow, numDig, numSym):
    uppercase = create_uppercase_letters_string()
    lowercase = create_lowercase_letters_string()
    digits = create_digits_string()
    symbols = create_symbols_string()

    length = numUp + numLow + numDig + numSym
    password = ""

    while len(password) < length:
        type = random.randint(0, 4)
        if type == 0 and numUp > 0:
            password += get_random_char_from_string(uppercase)
            numUp -= 1
        elif type == 1 and numLow > 0:
            password += get_random_char_from_string(lowercase)
            numLow -=  1
        elif type == 2 and numDig > 0:
            password += get_random_char_from_string(digits)
            numDig -= 1
        elif type == 3 and numSym > 0:
            password += get_random_char_from_string(symbols)
            numSym -= 1
        else:
            continue

    return password

def main():
    value = input("Enter four integer values, each separated by a space: ")
    tokens = value.split()
    length = len(tokens)
    if length < 4:
        print("Error: Too few values provided")
        exit()
    elif length > 4:
        print("Error: Too many values provided")
        exit()
    else:
        num_upper = int(tokens[0])
        num_lower = int(tokens[1])
        num_dig = int(tokens[2])
        num_sym = int(tokens[3])

        print(generate_random_password(num_upper, num_lower, num_dig, num_sym))


if __name__ == "__main__":
    main()