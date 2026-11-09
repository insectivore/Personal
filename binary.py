import math
import random

def menu():
    print("Welcome to the all-inclusive binary helper module.")
    print("1 - Randomized conversion practice questions")
    print("2 - Convert a value between bases")
    print("3 - Classic binary calculator")
    print("--------------------------------------------------")
    choice = input("Enter one of the numbers above to make a selection: ")
    if choice == "1":
        practice()
    elif choice == "2":
        convert()
    else:
        calculator()

def gen_binary():
    length = random.randint(3, 32)
    bits = ["1"]

    for x in range(length - 1):
        bits.append(str(random.randint(0, 1)))

    binary = int("".join(bits))

    return binary

def choose_type():
    choice = random.randint(1, 3)
    if choice == 1:
        type = "octal"
    elif choice == 2:
        type = "decimal"
    else:
        type = "hexadecimal"
    return type

def solve_octal(twobit):
    binary = str(twobit)
    remainder = len(binary) % 3

    if remainder != 0:
        padding = len(binary) + (3 - remainder)
        binary = binary.zfill(padding)

    chunks = []

    for index in range(0, len(binary), 3):
        chunk = binary[index : index + 3]
        chunks.append(chunk)

    octals = []

    for chunk in chunks:
        octal = int(chunk, 2)
        octals.append(octal)

    final = int("".join(str(d) for d in octals))

    return final

def solve_decimal(twobit):
    binary = str(twobit)

    chunks = []
    
    for index in range(0, len(binary), 1):
        chunk = binary[index : index + 1]
        chunks.append(chunk)

    all_bits = len(chunks)
    decimal_values = []

    for index in range(all_bits):
        bit = int(chunks[index])
        power = all_bits - 1 - index

        value = bit * int(math.pow(2, power))
        decimal_values.append(value)

    final = sum(decimal_values)

    return final

def solve_hex(twobit):
    binary = str(twobit)
    remainder = len(binary) % 4

    if remainder != 0:
        padding = len(binary) + (4 - remainder)
        binary = binary.zfill(padding)

    chunks = []

    for index in range(0, len(binary), 4):
        chunk = binary[index : index + 4]
        chunks.append(chunk)

    hexes = []

    for chunk in chunks:
        deci_val = int(chunk, 2)

        char = hex(deci_val)[2:].upper()
        hexes.append(char)

    final = "".join(hexes)

    return final

def practice():
    print("vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
    print("This is the looping randomized base-conversion practice module.")
    print("To exit at any time, simply hit the 'enter' key without entering a value.")
    print("-------------------------------------------------------------------------")
    
    while True:
        question = gen_binary()
        type = choose_type()

        print(f"\nConvert to {type}: {question}")

        if type == "octal":
            correct = solve_octal(question)
        elif type == "decimal":
            correct = solve_decimal(question)
        else:
            correct = solve_hex(question)

        response = input("Enter answer: ").strip()

        # Exit practice if user clicks enter key (empty string entered)
        if response == "":
            print("\nExiting practice...")
            break

        # Evaluate formatting and correct/incorrectness
        if type in ["octal", "decimal"]:
            try:
                response = int(response)
            except ValueError:
                print("Invalid format. Try again.")
                continue
        else: # in case of hexadecimal
            response = response.upper()

        if response == correct:
            print("Correct! Nya~")
        else:
            print("Incorrect. Correct answer:", correct)

    menu()

def convert():
    print("This is a WIP. Come back later.")
    go_back()

def calculator():
    print("This is a WIP. Come back later.")
    go_back()

def go_back():
    choice = input("Return to menu? [Y/N] ")
    if choice == "Y":
        menu()
    else:
        exit()

def main():
    menu()

if __name__ == "__main__":
    main()