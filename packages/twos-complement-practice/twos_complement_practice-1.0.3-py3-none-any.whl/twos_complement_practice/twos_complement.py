"""
Gamified practice tool for two's complement representation of
signed integers.

CS2210 Computer Organization
Clayton Cafiero <cbcafier@uvm.edu>

SPDX-License-Identifier: GPL-3.0-or-later
Copyright (C) 2025 Clayton Cafiero

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.

See <https://www.gnu.org/licenses/> for full license text.

"""
from collections import namedtuple, deque
import random

from colorama import Fore, Style, init as colorama_init


MIN_BITS = 3
MAX_BITS = 16
RECENT_CACHE_SIZE = 10
MAX_GEN_ATTEMPTS = 10


Parameters = namedtuple("Parameters", ["bits", "min", "max"])


def bin2dec(bs):
    """
    Converts a bitstring to an integer representation.

    >>> bin2dec('1011')
    -5
    >>> bin2dec('1110')
    -2
    >>> bin2dec('111011')
    -5
    >>> bin2dec('01110')
    14
    >>> bin2dec('000')
    0
    >>> bin2dec('1111')
    -1
    >>> bin2dec('0000001')
    1
    >>> bin2dec('cheddar')
    Traceback (most recent call last):
        ...
    ValueError: Bitstring must contain only '0' and '1'.
    >>> bin2dec('')
    Traceback (most recent call last):
        ...
    ValueError: Bitstring must be non-empty.
    """
    n = len(bs)
    if n == 0:
        raise ValueError("Bitstring must be non-empty.")
    if not all(c in '01' for c in bs):
        raise ValueError("Bitstring must contain only '0' and '1'.")
    value = int(bs, 2)
    if value & (1 << (n - 1)):  # sign bit is set
        value -= 1 << n         # apply two's complement
    return value


def dec2bin(d, bits_):
    """
    Converts a decimal value to a two's complement representation.

    >>> dec2bin(5, 5)
    '00101'
    >>> dec2bin(-5, 5)
    '11011'
    >>> dec2bin(1, 16)
    '0000000000000001'
    >>> dec2bin(-1, 16)
    '1111111111111111'
    >>> dec2bin(5, 0)
    Traceback (most recent call last):
        ...
    ValueError: Bit width must be a positive integer.
    """
    if bits_ <= 0:
        raise ValueError("Bit width must be a positive integer.")
    if not -(1 << (bits_ - 1)) <= d < (1 << (bits_ - 1)):
        raise ValueError("Value out of range for given bit width.")
    if d < 0:
        d = (1 << bits_) + d
    return f'{d:0{bits_}b}'


def prompt_with_validation(prompt, bit_width, parser):
    """
    Helper function to prompt user for values with validation.
    """
    while True:
        try:
            r = input(prompt)
        except EOFError:
            # This makes CLI robust to piped input or non-interactive use
            # e.g., for testing. A little hacky, but OK, I guess.
            print("\n[EOF received — exiting gracefully]")
            return None
        if r.lower() == 'q':
            return None
        if bit_width is not None and len(r) != bit_width:
            print(f"Invalid length! Expected {bit_width} bits.")
            continue
        try:
            return parser(r)
        except ValueError as e:
            print(e)


def play_additive_inverse(g_state, n):
    """
    User computes additive inverse of signed int.
    """
    n_as_bitstring = dec2bin(n, g_state['parameters'].bits)
    print(f"\nWhat's the additive inverse of {n_as_bitstring}?")
    prompt = "Enter bitstring (or 'q' to quit): "
    value = prompt_with_validation(prompt, g_state['parameters'].bits, bin2dec)
    if value is None:
        return False
    correct_answer = dec2bin(-n, g_state['parameters'].bits)
    if value == -n:
        g_state['results']['inverse']['correct'] += 1
        print(Fore.GREEN + "Correct!" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Incorrect!" + Style.RESET_ALL)
        print(f"The correct answer is {correct_answer}.")
        g_state['mistakes'].append(("inverse", n_as_bitstring, correct_answer))
    g_state['results']['inverse']['attempts'] += 1
    return True


def play_decimal_to_bitstring(g_state, n):
    """
    User converts decimal to bitstring.
    """
    print(f"\nWhat is decimal {n:d} as a two's complement bitstring?")
    prompt = "Enter bitstring (or 'q' to quit): "
    value = prompt_with_validation(prompt, g_state['parameters'].bits, bin2dec)
    if value is None:
        return False
    correct_answer = dec2bin(n, g_state['parameters'].bits)
    if value == n:
        g_state['results']['dec2bin']['correct'] += 1
        print(Fore.GREEN + "Correct!" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Incorrect!" + Style.RESET_ALL)
        print(f"The correct answer is {correct_answer}.")
        g_state['mistakes'].append(("dec2bin", str(n), correct_answer))
    g_state['results']['dec2bin']['attempts'] += 1
    return True


def play_bitstring_to_decimal(g_state, n):
    """
    User converts bitstring to decimal.
    """
    n_as_bitstring = dec2bin(n, g_state['parameters'].bits)
    print(f"\nWhat is {n_as_bitstring} as a decimal?")
    prompt = "Enter decimal value (or 'q' to quit): "
    value = prompt_with_validation(prompt, None, int)
    if value is None:
        return False
    if value == n:
        g_state['results']['bin2dec']['correct'] += 1
        print(Fore.GREEN + "Correct!" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Incorrect!" + Style.RESET_ALL)
        print(f"The correct answer is {n}.")
        g_state['mistakes'].append(("bin2dec", n_as_bitstring, str(n)))
    g_state['results']['bin2dec']['attempts'] += 1
    return True


def display_results(g_state):
    """
    Display results after user has asked to quit (before actually quitting).
    """
    print("\n***** RESULTS *****")
    total_attempts, total_correct = 0, 0
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
    p = g_state['parameters']
    print(f"\nWith {p.bits} bits, we can represent signed integers in the "
          f"interval [{p.min}, {p.max}].")
    print("\nYou will be asked a variety of questions about decimal and "
          "bitstring representations.")
    print("\t* I'll pick a random integer as a bitstring, and you provide "
          "the additive inverse as a bitstring.")
    print("\t* I'll pick a random integer as a bitstring, and you provide "
          "the decimal representation.")
    print("\t* I'll pick a random integer as a decimal and you provide "
          "the bitstring representation.")
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
                return bits
            print(f"Value must be between {MIN_BITS} and {MAX_BITS}.")
        except ValueError:
            print("Invalid input!")


def initialize_value_pools(minval, maxval):
    """
    Initialize the value pools.
    """
    values = list(range(minval, maxval + 1))
    return {
        'inverse': random.sample([v for v in values if v != minval],
                                 len(values) - 1),
        'dec2bin': random.sample(values, len(values)),
        'bin2dec': random.sample(values, len(values)),
    }


def draw_question(g_state, avoid_recent=True):
    """
    Helper function to draw a question.
    """
    attempts = 0
    while attempts < MAX_GEN_ATTEMPTS:
        mode = random.choice(['inverse', 'dec2bin', 'bin2dec'])
        if not g_state['value_pools'][mode]:
            values = range(g_state['parameters'].min,
                           g_state['parameters'].max + 1)
            if mode == 'inverse':
                values = [v for v in values if v != g_state['parameters'].min]
            g_state['value_pools'][mode] = random.sample(values, len(values))
        value = g_state['value_pools'][mode].pop()
        if not avoid_recent or (mode, value) not in g_state['recent']:
            return mode, value
        attempts += 1
    return None, None  # if all 10 tries failed


def get_next_question(g_state):
    """
    Get the next question, with some attempt at avoiding recent questions.
    """
    mode, value = draw_question(g_state, avoid_recent=True)
    if mode is None:
        # fallback to possibly repeated question
        mode, value = draw_question(g_state, avoid_recent=False)
    g_state['recent'].append((mode, value))
    if len(g_state['recent']) > RECENT_CACHE_SIZE:
        g_state['recent'].popleft()
    return mode, value


def _main():
    """
    Main exercise logic
    """
    colorama_init()
    print("\n***** TWO'S COMPLEMENT PRACTICE for SIGNED INTEGERS *****\n")
    bits = get_bits()
    minval = -(1 << (bits - 1))
    maxval = (1 << (bits - 1)) - 1

    game_state = {
        'parameters': Parameters(bits, minval, maxval),
        'results': {
            'inverse': {'attempts': 0, 'correct': 0,
                        'label': 'Additive inverse'},
            'dec2bin': {'attempts': 0, 'correct': 0,
                        'label': 'Decimal to binary'},
            'bin2dec': {'attempts': 0, 'correct': 0,
                        'label': 'Binary to decimal'}
        },
        'mistakes': [],
        'value_pools': initialize_value_pools(minval, maxval),
        'recent': deque()
    }

    display_instructions(game_state)

    keep_playing = True
    while keep_playing:
        mode, value = get_next_question(game_state)
        if mode is None:
            break
        if mode == 'inverse':
            keep_playing = play_additive_inverse(game_state, value)
        elif mode == 'dec2bin':
            keep_playing = play_decimal_to_bitstring(game_state, value)
        elif mode == 'bin2dec':
            keep_playing = play_bitstring_to_decimal(game_state, value)

    display_results(game_state)
    print("\nGoodbye!")


def run():
    """
    Entry point for importing and running from an IDE or script.
    """
    _main()


def main():
    """
    Entry point for the CLI console script.
    """
    _main()


if __name__ == '__main__':
    main()
