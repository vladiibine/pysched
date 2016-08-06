# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

import threading


class Scheduler(object):
    def __init__(self):
        registry = {}

    def schedule(self, callback, interval, args=None, kw=None):
        """Schedule the invocation of the callback with different options.

        :param callback: callable
        :param int|tuple|iterable interval:
            int: schedules the task to run repeatedly, forever, waiting
            `interval`
            tuple: (interval, times). Runs the task `times` times, at `interval`
            iterable: Callable that takes no arguments and returns an int,
                representing the number of seconds to wait until invoking the
                callback again.
        :param tuple|callable args:
            tuple: will forward it as *args when calling the callback function
            callable: will call it each time, and feed the results as *args
            to the
                callback function
        :param dict|callable kw: Same as `args`, but provide **kwargs to the
            callable
        :return: yields the results of the callable
        """
        if isinstance(interval, (int, float)):
            interval_func = create_interval_func(interval, 1)
        elif isinstance(interval, (list, tuple)):
            interval_func = create_interval_func(*interval)
        elif callable(interval):
            interval_func = interval
        else:
            raise TypeError(
                "Invalid type for parameter 'interval': {}"
                .format(type(interval)))

        next_interval = interval_func()
        while next_interval is not None:
            timer = threading.Timer(
                next_interval, callback, args=args or (), kwargs=kw or {})
            timer.start()
            next_interval = interval_func()


scheduler = Scheduler()


def create_interval_func(interval, times):
    def generate_intervals():
        for _ in range(times):
            yield interval

    class IntervalCallable(object):
        def __init__(self):
            self.interval_generator = generate_intervals()

        def __call__(self, *args, **kwargs):
            try:
                return next(self.interval_generator)
            except StopIteration:
                pass

    return IntervalCallable()

