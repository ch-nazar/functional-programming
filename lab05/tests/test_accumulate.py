import operator
from itertools import accumulate

from streams import prefix_stats


def test_accumulate_sum_prod():
    assert list(accumulate([1, 2, 3, 4])) == [1, 3, 6, 10]
    assert list(accumulate([1, 2, 3, 4], operator.mul)) == [1, 2, 6, 24]


def test_prefix_stats_use_accumulate():
    assert list(prefix_stats([4, 2, 6]))[-1] == (3, 12, 2, 6, 4.0)
