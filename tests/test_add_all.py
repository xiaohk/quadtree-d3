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


def test_add_all_10():
    xs = [
        -40.191,
        -55.385,
        88.971,
        73.954,
        -60.474,
        16.345,
        39.516,
        -13.811,
        97.217,
        -31.281,
    ]
    ys = [
        -37.354,
        77.688,
        -97.092,
        28.07,
        -54.189,
        -94.168,
        -29.653,
        -31.736,
        27.109,
        -44.638,
    ]

    assert Quadtree().add_all(xs, ys).root == [
        [
            [
                None,
                None,
                [
                    {"data": {"x": -60.474, "y": -54.189}},
                    None,
                    None,
                    [
                        None,
                        {"data": {"x": -31.281, "y": -44.638}},
                        {"data": {"x": -40.191, "y": -37.354}},
                        None,
                    ],
                ],
                None,
            ],
            {"data": {"x": 16.345, "y": -94.168}},
            {"data": {"x": -13.811, "y": -31.736}},
            {"data": {"x": 39.516, "y": -29.653}},
        ],
        [
            {"data": {"x": 88.971, "y": -97.092}},
            None,
            [
                None,
                None,
                [
                    None,
                    None,
                    {"data": {"x": 73.954, "y": 28.07}},
                    {"data": {"x": 97.217, "y": 27.109}},
                ],
                None,
            ],
            None,
        ],
        {"data": {"x": -55.385, "y": 77.688}},
        None,
    ]


def test_random_extent_before_add_all():
    xs = [
        -40.191,
        -55.385,
        88.971,
        73.954,
        -60.474,
        16.345,
        39.516,
        -13.811,
        97.217,
        -31.281,
    ]
    ys = [
        -37.354,
        77.688,
        -97.092,
        28.07,
        -54.189,
        -94.168,
        -29.653,
        -31.736,
        27.109,
        -44.638,
    ]

    q = (
        Quadtree()
        .extent([-72.51409999999998, -100.5876], [109.2571, 81.1836])
        .add_all(xs, ys)
    )

    assert q.root == [
        [
            [
                None,
                None,
                {"data": {"x": -60.474, "y": -54.189}},
                [
                    None,
                    None,
                    [
                        None,
                        None,
                        {"data": {"x": -40.191, "y": -37.354}},
                        {"data": {"x": -31.281, "y": -44.638}},
                    ],
                    None,
                ],
            ],
            {"data": {"x": 16.345, "y": -94.168}},
            {"data": {"x": -13.811, "y": -31.736}},
            {"data": {"x": 39.516, "y": -29.653}},
        ],
        {"data": {"x": 88.971, "y": -97.092}},
        {"data": {"x": -55.385, "y": 77.688}},
        [
            [
                {"data": {"x": 73.954, "y": 28.07}},
                {"data": {"x": 97.217, "y": 27.109}},
                None,
                None,
            ],
            None,
            None,
            None,
        ],
    ]
