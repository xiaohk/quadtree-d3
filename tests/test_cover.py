#!/usr/bin/env python

"""Tests for `quadtreed3` package."""

import pytest
from quadtreed3.quadtreed3 import Quadtree


@pytest.fixture
def quadtree():
    quadtree = Quadtree()
    return quadtree


def test_content_trivial(quadtree: Quadtree):
    assert quadtree.cover(1, 2).extent() == [[1, 2], [2, 3]]


def test_content_non_trivial(quadtree: Quadtree):
    assert quadtree.cover(0, 0).cover(1, 2).extent() == [[0, 0], [4, 4]]


def test_content_double():
    assert Quadtree().cover(0, 0).cover(2, 2).cover(-1, -1).extent() == [
        [-4, -4],
        [4, 4],
    ]
    assert Quadtree().cover(0, 0).cover(2, 2).cover(1, -1).extent() == [[0, -4], [8, 4]]
    assert Quadtree().cover(0, 0).cover(2, 2).cover(3, -1).extent() == [[0, -4], [8, 4]]
    assert Quadtree().cover(0, 0).cover(2, 2).cover(3, 1).extent() == [[0, 0], [4, 4]]
    assert Quadtree().cover(0, 0).cover(2, 2).cover(3, 3).extent() == [[0, 0], [4, 4]]
    assert Quadtree().cover(0, 0).cover(2, 2).cover(1, 3).extent() == [[0, 0], [4, 4]]
    assert Quadtree().cover(0, 0).cover(2, 2).cover(-1, 3).extent() == [[-4, 0], [4, 8]]
    assert Quadtree().cover(0, 0).cover(2, 2).cover(-1, 1).extent() == [[-4, 0], [4, 8]]
    assert Quadtree().cover(0, 0).cover(2, 2).cover(-3, -3).extent() == [
        [-4, -4],
        [4, 4],
    ]
    assert Quadtree().cover(0, 0).cover(2, 2).cover(3, -3).extent() == [[0, -4], [8, 4]]
    assert Quadtree().cover(0, 0).cover(2, 2).cover(5, -3).extent() == [[0, -4], [8, 4]]
    assert Quadtree().cover(0, 0).cover(2, 2).cover(5, 3).extent() == [[0, 0], [8, 8]]
    assert Quadtree().cover(0, 0).cover(2, 2).cover(5, 5).extent() == [[0, 0], [8, 8]]
    assert Quadtree().cover(0, 0).cover(2, 2).cover(3, 5).extent() == [[0, 0], [8, 8]]
    assert Quadtree().cover(0, 0).cover(2, 2).cover(-3, 5).extent() == [[-4, 0], [4, 8]]
    assert Quadtree().cover(0, 0).cover(2, 2).cover(-3, 3).extent() == [[-4, 0], [4, 8]]
