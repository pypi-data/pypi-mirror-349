"""
Test for get_next_question()

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
from collections import deque

from twos_complement_practice.twos_complement import (initialize_value_pools,
                                                      get_next_question,
                                                      Parameters)


def test_initialize_value_pools_excludes_min_for_inverse():
    """
    Test initialization of value pools (used to reduce likelihood of
    questions being repeated.
    """
    minval = -4
    maxval = 3
    pools = initialize_value_pools(minval, maxval)
    assert minval not in pools['inverse']
    assert set(pools['dec2bin']) == set(range(minval, maxval + 1))
    assert set(pools['bin2dec']) == set(range(minval, maxval + 1))


def test_get_next_question_populates_recent():
    """
    Test behavior of get_next_question() interaction with cache.
    """
    g_state = {
        'parameters': Parameters(3, -4, 3),
        'value_pools': initialize_value_pools(-4, 3),
        'recent': deque(),
        'results': {'inverse': {}, 'dec2bin': {}, 'bin2dec': {}},
        'mistakes': []
    }

    mode, value = get_next_question(g_state)
    assert (mode, value) in g_state['recent']
    assert mode in ['inverse', 'dec2bin', 'bin2dec']
    assert isinstance(value, int)


def test_get_next_question_all_recent():
    """
    Force the `recent` cache to saturate and verify the fallback logic
    still returns a usable value.
    """
    g_state = {
        'parameters': Parameters(3, -4, 3),
        'value_pools': {
            'inverse': [-3, -2],
            'dec2bin': [-4],
            'bin2dec': [0]
        },
        'recent': deque([('inverse', -3), ('inverse', -2),
                         ('dec2bin', -4), ('bin2dec', 0)],
                        maxlen=10),
        'results': {'inverse': {}, 'dec2bin': {}, 'bin2dec': {}},
        'mistakes': []
    }

    mode, value = get_next_question(g_state)
    assert mode in ['inverse', 'dec2bin', 'bin2dec']
    assert isinstance(value, int)
