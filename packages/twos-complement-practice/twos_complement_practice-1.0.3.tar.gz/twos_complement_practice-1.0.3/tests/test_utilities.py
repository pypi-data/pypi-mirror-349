"""
Tests for pure utility functions

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
import pytest

from twos_complement_practice.twos_complement import bin2dec, dec2bin


@pytest.mark.parametrize("bitstring, expected", [
    ('000', 0),
    ('001', 1),
    ('010', 2),
    ('111', -1),
    ('1000', -8),
    ('0111', 7),
    ('000001', 1),
])
def test_bin2dec_basic(bitstring, expected):
    """
    Test bin2dec
    """
    assert bin2dec(bitstring) == expected


def test_bin2dec_invalid():
    """
    Test bin2dec to ensure expected exceptions are raised.
    """
    with pytest.raises(ValueError, match="only '0' and '1'"):
        bin2dec("10a1")
    with pytest.raises(ValueError, match="non-empty"):
        bin2dec("")


@pytest.mark.parametrize("decimal, bit_width, expected", [
    (1, 3, '001'),
    (-1, 3, '111'),
    (-4, 3, '100'),
    (-2, 5, '11110'),
    (0, 16, '0000000000000000'),
])
def test_dec2bin_basic(decimal, bit_width, expected):
    """
    Test dec2bin
    """
    assert dec2bin(decimal, bit_width) == expected


def test_dec2bin_range_error():
    """
    Test dec2bin to ensure expected exceptions are raised.
    """
    with pytest.raises(ValueError, match="range"):
        dec2bin(5, 3)
    with pytest.raises(ValueError, match="positive integer"):
        dec2bin(5, 0)
