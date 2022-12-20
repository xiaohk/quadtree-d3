#!/usr/bin/env python

"""Tests for `quadtreed3` package."""

from quadtreed3 import Quadtree


def test_add_simple():
    q = Quadtree()

    assert q.add(0, 0).root == {"data": {"x": 0, "y": 0}}
    assert q.add(0.9, 0.9).root == [
        {"data": {"x": 0, "y": 0}},
        None,
        None,
        {"data": {"x": 0.9, "y": 0.9}},
    ]

    assert q.add(0.9, 0.0).root == [
        {"data": {"x": 0, "y": 0}},
        {"data": {"x": 0.9, "y": 0}},
        None,
        {"data": {"x": 0.9, "y": 0.9}},
    ]

    assert q.add(0.0, 0.9).root == [
        {"data": {"x": 0, "y": 0}},
        {"data": {"x": 0.9, "y": 0}},
        {"data": {"x": 0, "y": 0.9}},
        {"data": {"x": 0.9, "y": 0.9}},
    ]

    assert q.add(0.4, 0.4).root == [
        [{"data": {"x": 0, "y": 0}}, None, None, {"data": {"x": 0.4, "y": 0.4}}],
        {"data": {"x": 0.9, "y": 0}},
        {"data": {"x": 0, "y": 0.9}},
        {"data": {"x": 0.9, "y": 0.9}},
    ]


def test_add_perimeter():
    q = Quadtree()
    assert q.add(0, 0).root == {"data": {"x": 0, "y": 0}}
    assert q.add(1, 1).root == [
        {"data": {"x": 0, "y": 0}},
        None,
        None,
        {"data": {"x": 1, "y": 1}},
    ]
    assert q.add(1, 0).root == [
        {"data": {"x": 0, "y": 0}},
        {"data": {"x": 1, "y": 0}},
        None,
        {"data": {"x": 1, "y": 1}},
    ]
    assert q.add(0, 1).root == [
        {"data": {"x": 0, "y": 0}},
        {"data": {"x": 1, "y": 0}},
        {"data": {"x": 0, "y": 1}},
        {"data": {"x": 1, "y": 1}},
    ]


def test_add_top():
    q = Quadtree().extent([0, 0], [2, 2])
    assert q.add(1, -1).extent() == [[0, -4], [8, 4]]


def test_add_right():
    q = Quadtree().extent([0, 0], [2, 2])
    assert q.add(3, 1).extent(), [[0, 0], [4, 4]]


def test_add_bottom():
    q = Quadtree().extent([0, 0], [2, 2])
    assert q.add(1, 3).extent() == [[0, 0], [4, 4]]


def test_add_left():
    q = Quadtree().extent([0, 0], [2, 2])
    assert q.add(-1, 1).extent() == [[-4, 0], [4, 8]]


def test_add_same_point():
    q = Quadtree().extent([0, 0], [1, 1])
    assert q.add(0, 0).root == {"data": {"x": 0, "y": 0}}
    assert q.add(1, 0).root == [
        {"data": {"x": 0, "y": 0}},
        {"data": {"x": 1, "y": 0}},
        None,
        None,
    ]
    assert q.add(0, 1).root == [
        {"data": {"x": 0, "y": 0}},
        {"data": {"x": 1, "y": 0}},
        {"data": {"x": 0, "y": 1}},
        None,
    ]
    assert q.add(0, 1).root == [
        {"data": {"x": 0, "y": 0}},
        {"data": {"x": 1, "y": 0}},
        {"data": {"x": 0, "y": 1}, "next": {"data": {"x": 0, "y": 1}}},
        None,
    ]


def test_add_first_point():
    q = Quadtree().add(1, 2)
    assert q.extent() == [[1, 2], [2, 3]]
    assert q.root == {"data": {"x": 1, "y": 2}}
