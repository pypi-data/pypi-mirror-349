"""
Gamified practice tool for two's complement representation of
signed integers.

CS2210 Computer Organization
Clayton Cafiero <cbcafier@uvm.edu>

SPDX-License-Identifier: GPL-3.0-or-later
Copyright (C) 2024 Clayton Cafiero

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.

See <https://www.gnu.org/licenses/> for full license text.

"""
from collections import namedtuple
import random
from colorama import Fore, Style, init as colorama_init


MIN_BITS = 3
MAX_BITS = 16

Parameters = namedtuple("Parameters", ["bits", "min", "max"])


def bin2dec(bs):
    """
    Converts a bitstring to an integer representation.
    """
    n = len(bs)  # bs is bitstring
    if not all(c in '01' for c in bs):
        raise ValueError("Bitstring must contain only '0' and '1'.")
    value = int(bs, 2)
    if value & (1 << (n - 1)):  # sign bit is set
        value -= 1 << n  # apply two's complement
    return value


def dec2bin(d, bits_):
    """
    Converts a decimal value to a two's complement representation.
    """
    if not -(1 << (bits_ - 1)) <= d < (1 << (bits_ - 1)):
        raise ValueError("Value out of range for given bit width.")
    if d < 0:
        d = (1 << bits_) + d
    return f'{d:0{bits_}b}'


def prompt_until_valid(prompt, bits_, parser):
    """
    Helper function to prompt user for values with validation.
    """
    while True:
        r = input(prompt)
        if r.lower() == 'q':
            return None
        if bits_ is not None and len(r) != bits_:
            print(f"Invalid length! Expected {bits_} bits.")
            continue
        try:
            return parser(r)
        except ValueError as e:
            print(e)


def play_additive_inverse(g_state):
    """
    User computes additive inverse of signed int.
    """
    n = random.randint(g_state['parameters'].min + 1,
                       g_state['parameters'].max)
    n_as_bitstring = dec2bin(n, g_state['parameters'].bits)
    print(f"\nWhat's the additive inverse of {n_as_bitstring}?")
    prompt = "Enter bitstring (or 'q' to quit): "
    value = prompt_until_valid(prompt, g_state['parameters'].bits, bin2dec)
    if value is None:
        return False
    correct_answer = dec2bin(-n, g_state['parameters'].bits)
    if value == -n:
        g_state['results']['inverse']['correct'] += 1
        print(Fore.GREEN + "Correct!" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Incorrect!" + Style.RESET_ALL)
        print(f"The correct answer is {correct_answer}.")
        g_state['mistakes'].append(
            ("inverse", n_as_bitstring, correct_answer)
        )
    g_state['results']['inverse']['attempts'] += 1
    return True


def play_decimal_to_bitstring(g_state):
    """
    User converts decimal to bitstring.
    """
    n = random.randint(g_state['parameters'].min,
                       g_state['parameters'].max)
    print(f"\nWhat is decimal {n:d} as a two's complement bitstring?")
    prompt = "Enter bitstring (or 'q' to quit): "
    value = prompt_until_valid(prompt, g_state['parameters'].bits, bin2dec)
    if value is None:
        return False
    correct_answer = dec2bin(n, g_state['parameters'].bits)
    if value == n:
        g_state['results']['dec2bin']['correct'] += 1
        print(Fore.GREEN + "Correct!" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Incorrect!" + Style.RESET_ALL)
        print(f"The correct answer is {correct_answer}.")
        g_state['mistakes'].append(
            ("dec2bin", str(n), correct_answer)
        )
    g_state['results']['dec2bin']['attempts'] += 1
    return True


def play_bitstring_to_decimal(g_state):
    """
    User converts bitstring to decimal.
    """
    n = random.randint(g_state['parameters'].min,
                       g_state['parameters'].max)
    n_as_bitstring = dec2bin(n, g_state['parameters'].bits)  # safe
    print(f"\nWhat is {n_as_bitstring} as a decimal?")
    prompt = "Enter decimal value (or 'q' to quit): "
    value = prompt_until_valid(prompt, None, int)
    if value is None:
        return False
    if value == n:
        g_state['results']['bin2dec']['correct'] += 1
        print(Fore.GREEN + "Correct!" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Incorrect!" + Style.RESET_ALL)
        print(f"The correct answer is {n}.")
        g_state['mistakes'].append(
            ("bin2dec", n_as_bitstring, str(n))
        )
    g_state['results']['bin2dec']['attempts'] += 1
    return True


def display_results(g_state):
    """
    Display results after user has asked to quit (before actually quitting).
    """
    print("\n***** RESULTS *****")
    total_attempts = 0
    total_correct = 0
    for result in g_state['results'].values():
        total_attempts += result['attempts']
        total_correct += result['correct']
        if result['attempts']:
            print(f"\n{result['label']}:")
            print(f"\t{result['correct']} / {result['attempts']} "
                  f"= {result['correct'] / result['attempts']:.1%}")
    if total_attempts:
        print(f"\nOverall score: {total_correct} / {total_attempts} "
              f"= {total_correct / total_attempts:.1%}")
    else:
        print("Nothing attempted!")

    if g_state['mistakes']:
        print("\nMistakes:")
        for mode, prompt, correct in g_state['mistakes']:
            print(f"\t[{mode}] {prompt} → {correct}")


def display_instructions(g_state):
    """
    Display instructions.
    """
    print(f"\nWith {g_state['parameters'].bits} bits, we can represent "
          f"signed integers in the interval [{g_state['parameters'].min:,d}, "
          f"{g_state['parameters'].max:,d}].")
    print("\nI'll pick a random integer in the interval "
          f"[{g_state['parameters'].min + 1:,}, "
          f"{g_state['parameters'].max:,}] and display "
          "it as a bitstring,\nthen you give me the additive inverse as a "
          "bitstring.")
    print("\nOR")
    print("\nI'll pick a random integer in the interval "
          f"[{g_state['parameters'].min:,}, "
          f"{g_state['parameters'].max:,}] and display it "
          "as a decimal,\nthen you give me the binary (bitstring) "
          "representation.")
    print("\nOR")
    print("\nI'll pick a random integer in the interval "
          f"[{g_state['parameters'].min:,}, "
          f"{g_state['parameters'].max:,}] and display it "
          "as a bitstring,\nthen you give me the decimal representation.")
    print()
    input("Press Enter to continue...")


def get_bits():
    """
    Get number of bits in permissible range.
    """
    while True:
        r = input(f"Enter number of bits ({MIN_BITS}--{MAX_BITS}): ")
        try:
            bits = int(r)
            if MIN_BITS <= bits <= MAX_BITS:
                break
            print(f"Value must be between {MIN_BITS} and {MAX_BITS} (inclusive).")
        except ValueError:
            print('Invalid input!')
    return bits


def _main():
    """
    Main exercise logic
    """

    OPTIONS = [play_additive_inverse,
               play_decimal_to_bitstring,
               play_bitstring_to_decimal]

    colorama_init()

    print("\n***** TWO'S COMPLEMENT PRACTICE for SIGNED INTEGERS *****\n")

    game_state = {'parameters': Parameters(bits := get_bits(),
                                           -(2 ** (bits - 1)),  # min
                                           2 ** (bits - 1) - 1),  # max
                  'results': {
                      'inverse': {'attempts': 0,
                                  'correct': 0,
                                  'label': 'Additive inverse'},
                      'dec2bin': {'attempts': 0,
                                  'correct': 0,
                                  'label': 'Decimal to binary'},
                      'bin2dec': {'attempts': 0,
                                  'correct': 0,
                                  'label': 'Binary to decimal'}},
                  'mistakes': []}

    display_instructions(game_state)

    keep_playing = True

    while keep_playing:
        keep_playing = random.choice(OPTIONS)(game_state)

    display_results(game_state)

    print("\nGoodbye!")


def run():
    """Entry point for importing and running from an IDE or script."""
    _main()


def main():
    """Entry point for the CLI console script."""
    _main()


if __name__ == '__main__':
    main()
