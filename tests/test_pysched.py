#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pysched
----------------------------------

Tests for `pysched` module.
"""


import sys
import unittest
import time

import mock

from pysched import pysched


def noop(*args, **kwargs):
    pass


class TimeFaker(object):
    """Used for faking the passage of time"""
    def __init__(self, increment=10):
        self.dummy_time = 0
        self.increment = increment

    def __call__(self, *args, **kwargs):
        try:
            return self.dummy_time
        finally:
            self.dummy_time += self.increment


class TestPysched(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_run_single_task(self):
        # This test works in py2.7 but they changed the threading module a lot
        # in py3.5, so this will probably fail in other python versions too
        state = []

        def callback():
            state.append(1)

        scheduler = pysched.Scheduler()

        with mock.patch('threading._sleep', noop):
            with mock.patch('threading._time', TimeFaker(1000)):
                scheduler.schedule(callback, (1, 1))
                time.sleep(.1)  # to make sure the timer thread wakes up

        self.assertListEqual(state, [1])


if __name__ == '__main__':
    sys.exit(unittest.main())
