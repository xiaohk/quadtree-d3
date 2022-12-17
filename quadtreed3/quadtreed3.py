"""Main module."""


from glob import glob
from os.path import exists, join, basename
from tqdm import tqdm
from json import load, dump, JSONEncoder, dumps

from collections import Counter
from copy import deepcopy
from typing import Union, Optional

import numpy as np

import time
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

        pass

    def add_all_data(self, data: list[dict]):
        """
        Add all data points into the quadtree.

        Args:
            data(list[dict]): A list of data entries. Each data entry is a
                dictionary with at least two keys 'x' and 'y'.
        """
        pass

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
        pass

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
            self.root = node

        # Record the extent
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1

        return self
