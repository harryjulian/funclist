from funclist.src import funclist
import pytest
import random
from itertools import tee
from hypothesis import given
import hypothesis.strategies as st


def _pairwise(iterable):
    "Util: s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return list(zip(a, b))


def test_init_literal():
    fl = funclist(1, 2, 3, 4)
    assert fl == [1, 2, 3, 4]


def test_init_list():
    fl = funclist([1, 2, 3, 4])
    assert fl == [1, 2, 3, 4]


@given(st.lists(st.integers()), st.lists(st.integers(), max_size = 5))
def test_append(ls: list, to_append: list):
    fl = funclist(ls)
    for i in to_append:
        ls.append(i)
        fl = fl.append(i)
        assert fl == ls


@given(st.lists(st.integers(), min_size = 10, max_size = 200))
def test_remove(ls: list):
    fl = funclist(ls)
    for _ in range(int(len(ls) / 4)):
        elem = random.choice(ls)
        ls.remove(elem)
        fl = fl.remove(elem)
        assert fl == ls


@given(st.lists(st.integers()), st.lists(st.integers(), max_size = 5))
def test_extend(ls: list, to_extend: list):
    fl = funclist(ls).extend(to_extend)
    ls.extend(to_extend)
    assert fl == ls


@given(st.lists(st.integers(), min_size = 5, max_size = 100))
def test_pop(ls: list):
    fl = funclist(ls)
    for _ in range(int(len(ls) / 4)):
        idx = random.choice([i for i in range(len(ls))])
        fl = fl.pop(idx)
        ls.pop(idx)
        assert fl == ls


@given(st.lists(st.integers(), max_size = 100))
def test_reverse(ls: list):
    fl = funclist(ls).reverse()
    ls.reverse()
    assert fl == ls


@given(st.lists(st.integers(), max_size = 100))
def test_sort(ls: list):
    fl = funclist(ls).sort()
    ls = sorted(ls)
    assert fl == ls


@given(st.lists(st.integers(), max_size = 100))
def test_filter(ls: list):
    f = lambda x: x % 2 == 0
    fl = funclist(ls).filter(f)
    ls = list(filter(f, ls))
    assert fl == ls


@given(st.lists(st.lists(st.integers(), max_size = 100)))
def test_flatten(ls: list):
    fl = funclist(ls).flatten()
    for i in fl:
        assert not isinstance(i, list)


@given(st.lists(st.integers(), max_size = 100))
def test_enumerate(ls: list):
    fl = funclist(ls).enumerate()
    for l_enum, fl_enum in zip(enumerate(ls), fl):
        assert l_enum == fl_enum


@given(st.lists(st.integers(), max_size = 100))
def test_map(ls: list):
    func = lambda x: x * 2
    fl = funclist(ls).map(func)
    expected = [i * 2 for i in ls]
    assert fl == expected


@given(st.lists(st.integers(), max_size = 100))
def test_dedupe(ls: list):
    n = ls + ls.copy()
    fl = funclist(n).dedupe()
    assert(len(set(fl)) == len(fl))


@given(st.lists(st.integers(), max_size = 100))
def test_windows(ls: list):
    fl = funclist(ls).windows(2)
    ls = _pairwise(ls)
    for _ in zip(fl, ls):
        assert fl == ls