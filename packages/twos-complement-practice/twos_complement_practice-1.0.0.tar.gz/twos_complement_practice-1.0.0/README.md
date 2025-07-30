# Two's Complement Practice Tool

This is a command-line tool for practicing and reviewing two's complement representation of signed integers.

Developed for CS2210 (Computer Organization) at the University of Vermont by [Clayton Cafiero](mailto:cbcafier@uvm.edu).

---

## Installation

```bash
pip install twos-complement-practice
```

---

## Usage

After installing:

```bash
twos-practice
```

You will be prompted to choose a bit width (_e.g._, 4, 8, etc.). The program will then randomly select from three activity types:

- **Additive inverse**: Given a bitstring, provide the additive inverse in two's complement form.
- **Decimal to bitstring**: Convert a signed decimal integer to two's complement binary.
- **Bitstring to decimal**: Convert a two's complement binary string to a decimal integer.

You can exit at any prompt by typing `q`.

At the end, you'll get a summary of your performance and a list of any incorrect responses.

---

## Educational goals

This tool is designed to:

- reinforce understanding of signed binary number representation,
- develop fluency with two's complement conversions, and
- provide low-stakes, interactive feedback for learners.

---

## License

This project is licensed under the terms of the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html).

You are free to use, modify, and distribute this software under the conditions specified in the license.

> © 2025 Clayton Cafiero  
> For inquiries, contact [cbcafier@uvm.edu](mailto:cbcafier@uvm.edu)

---

## Dependencies

- [colorama](https://pypi.org/project/colorama/): for cross-platform colored terminal output.
