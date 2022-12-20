"""Main module."""

from tqdm import tqdm
from json import load, dump

from typing import Union

import numpy as np

import math


class Quadtree:
    def __init__(self):
        # The tree is fully initialized after self.add_all() call
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.root = None

    def add(self, x: float, y: float, d: Union[dict, None] = None):
        """
        Add a data point into the quadtree.

        Args:
            x(float): The x coordinate of the data point
            y(float): The y coordinate of the data point
            d(dict): The data entry associated with this data point. The default
                value is {'x': x, 'y': y}.
        """

        # Make sure the new point is covered by the extent before adding it
        self.cover(x, y)
        self._add_skip_cover(x, y, d)
        return self

    def _add_skip_cover(self, x: float, y: float, d: Union[dict, None] = None):
        """
        Add a data point into the quadtree without covering it first. This method
        should only be called in add(), add_all_data() or add_all()

        Args:
            x(float): The x coordinate of the data point
            y(float): The y coordinate of the data point
            d(dict): The data entry associated with this data point. The default
                value is {'x': x, 'y': y}.
        """

        # Create a leaf node
        if d:
            leaf = {"data": d}
        else:
            leaf = {"data": {"x": x, "y": y}}

        # There are three cases when adding a new point to a quadtree.
        # (1) The tree is empty => use this new point as the root
        # (2) Find the node this point should goes to => if there is no point
        # in the slot => add this point
        # (3) Find the node this point should goes to => if there is already a
        # point => split the node repetitively until two points are separated
        # => add this point

        # Case (1)
        if self.root is None:
            self.root = leaf
            return self

        # Case (2) & (3)
        # Find the node this data point belongs to (2D Binary search)
        node = self.root
        x0, y0, x1, y1 = self.x0, self.y0, self.x1, self.y1
        parent = None
        quad = None

        while "data" not in node:
            xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
            quad = get_quadrant(x, y, xm, ym)
            # Quadrant index
            # |2|3|
            # |0|1|

            if quad == 3:
                x0, y0 = xm, ym

            elif quad == 2:
                x1, y0 = xm, ym

            elif quad == 1:
                x0, y1 = xm, ym

            else:
                x1, y1 = xm, ym

            parent = node
            node = parent[quad]

            # Case (2): Empty slot to plug in this data point
            if node is None:
                parent[quad] = leaf
                return self

        # Case (3): The current `node` is a leaf node where the data point
        # should go to. First check if the current `node` shares the exact x
        # and y for the data point
        x_old, y_old = node["data"]["x"], node["data"]["y"]

        if x == x_old and y == y_old:
            # Link these two points
            leaf["next"] = node
            if parent is None:
                self.root = leaf
            else:
                parent[quad] = leaf
            return self

        # If two points are not the same, we keep splitting the current node
        # until two data points are separated in different quadrants
        quad_new = quad
        quad_old = quad

        while quad_new == quad_old:
            if parent is None:
                self.root = [None for _ in range(4)]
                parent = self.root
            else:
                parent[quad_new] = [None for _ in range(4)]
                parent = parent[quad_new]

            # Get the new quadrants for the new and old points
            xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
            quad_new = get_quadrant(x, y, xm, ym)
            quad_old = get_quadrant(x_old, y_old, xm, ym)

            if quad_new == 3:
                x0, y0 = xm, ym

            elif quad_new == 2:
                x1, y0 = xm, ym

            elif quad_new == 1:
                x0, y1 = xm, ym

            else:
                x1, y1 = xm, ym

        # Insert two nodes as leaves in two different quadrants
        parent[quad_old] = node
        parent[quad_new] = leaf
        return self

    def add_all_data(self, data: list[dict]):
        """
        Add all data points into the quadtree.

        Args:
            data(list[dict]): A list of data entries. Each data entry is a
                dictionary with at least two keys 'x' and 'y'.
        """

        xs, ys = [], []
        new_data = []

        for d in data:
            xs.append(d["x"])
            ys.append(d["y"])
            new_data.append(d)

        self.add_all(xs, ys, new_data)
        return self

    def add_all(
        self, xs: list[float], ys: list[float], data: Union[list[dict], None] = None
    ):
        """
        Add all data points into the quadtree. This function is a syntax sugar
        for this.add_all_data().

        Args:
            xs(list[float]): A list of x coordinates
            ys(list[float]): A list of y coordinates
            data(list[dict]): A list of data entries. Each data entry is a
                dictionary with at least two keys 'x' and 'y'.
        """

        # Initialize the extent by (min_x, min_y) and (max_x, max_y)
        x0, y0, x1, y1 = np.min(xs), np.min(ys), np.max(xs), np.max(ys)

        if x0 > x1 or y0 > y1:
            return self

        self.cover(x0, y0)
        self.cover(x1, y1)

        # Add new points one by one
        for i, _ in tqdm(enumerate(xs)):
            self.add(xs[i], ys[i], data[i] if data else None)

        return self

    def extent(
        self, point0: list[float, float] = None, point1: list[float, float] = None
    ) -> list[list[float, float], list[float, float]]:
        """Set the extent for this quadtree or get the current extent.

        Args:
            point0 (list[float, float], optional): Origin coordinate. Defaults to None.
            point1 (list[float, float], optional): Extent point coordinate. Defaults to None.

        Returns:
            list[list[float, float], list[float, float]]: Current extent [origin, extent]
        """
        if point0 is None:
            return [
                [self.x0, self.y0],
                [self.x1, self.y1],
            ]
        else:
            self.cover(point0[0], point0[1])
            self.cover(point1[0], point1[1])
            return self

    def cover(self, x: float, y: float):
        """
        Extend the current boundaries to cover the data point (x, y).

        Args:
            x(float): The x coordinate of the data point
            y(float): The y coordinate of the data point
        """

        x0, y0, x1, y1 = self.x0, self.y0, self.x1, self.y1

        # Initialize the extent if there is none, make sure the extent is always
        # integer values
        if x0 is None:
            x0 = int(math.floor(x))
            y0 = int(math.floor(y))
            x1 = x0 + 1
            y1 = y0 + 1

        else:
            # Cover the new point by extending the boundaries symmetrically
            length = x1 - x0
            node = self.root

            while x < x0 or x >= x1 or y < y0 or y >= y1:
                # Quadrant index
                # |2|3|
                # |0|1|
                length *= 2
                parent = [None for _ in range(4)]

                if x < x0 and y < y0:
                    # Point is at bottom left, the original extent will be at top right
                    parent[3] = node
                    node = parent

                    x0 = x1 - length
                    y0 = y1 - length

                elif x >= x0 and y < y0:
                    # Point is at bottom, the original extent will be at top
                    parent[2] = node
                    node = parent

                    x1 = x0 + length
                    y0 = y1 - length

                elif x < x0 and y >= y0:
                    # Point is at left, the original extent will be at bottom right
                    parent[1] = node
                    node = parent

                    x0 = x1 - length
                    y1 = y0 + length

                else:
                    # Point is in range in terms of (x0, y0), the original extent
                    # will be at the bottom left
                    parent[0] = node
                    node = parent

                    x1 = x0 + length
                    y1 = y0 + length

            # Update the root to point to the root node
            if self.root is not None and "data" not in self.root:
                self.root = node

        # Record the extent
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1

        return self


def get_quadrant(x: float, y: float, xm: float, ym: float) -> int:
    """
    Get the quadrant index for (x, y). The quadrant order is defined by lower x
    to larger x, and lower y to larger y.

    |2|3|\n
    |0|1|

    Args:
        x (float): The x coordinate of point (x, y)
        y (float): The y coordinate of point (x, y)
        xm (float): The x coordinate of the midpoint of a square
        ym (float): The y coordinate of the midpoint of a square

    Returns:
        int: Quadrant index
    """
    if x >= xm and y >= ym:
        return 3

    elif x < xm and y >= ym:
        return 2

    elif x >= xm and y < ym:
        return 1

    else:
        return 0
