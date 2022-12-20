#!/usr/bin/env python

"""Tests for `quadtreed3` package."""

from quadtreed3.quadtreed3 import Quadtree


def test_add_all_simple():
    q = Quadtree()
    xs = [0.0, 0.9, 0.9, 0.0, 0.4]
    ys = [0.0, 0.9, 0.0, 0.9, 0.4]
    q.add_all(xs, ys)
    assert q.root == [
        [{"data": {"x": 0, "y": 0}}, None, None, {"data": {"x": 0.4, "y": 0.4}}],
        {"data": {"x": 0.9, "y": 0}},
        {"data": {"x": 0, "y": 0.9}},
        {"data": {"x": 0.9, "y": 0.9}},
    ]


def test_extent_before_adding():
    q = Quadtree().add_all([0.4, 0, 0.9], [0.4, 0, 0.9])
    assert q.root == [
        [{"data": {"x": 0, "y": 0}}, None, None, {"data": {"x": 0.4, "y": 0.4}}],
        None,
        None,
        {"data": {"x": 0.9, "y": 0.9}},
    ]


def test_add_all_data():
    xs = [0.4, 0, 0.9]
    ys = [0.4, 0, 0.9]
    data = []

    for i, _ in enumerate(xs):
        data.append({"x": xs[i], "y": ys[i]})

    q = Quadtree().add_all_data(data)
    assert q.root == [
        [{"data": {"x": 0, "y": 0}}, None, None, {"data": {"x": 0.4, "y": 0.4}}],
        None,
        None,
        {"data": {"x": 0.9, "y": 0.9}},
    ]
