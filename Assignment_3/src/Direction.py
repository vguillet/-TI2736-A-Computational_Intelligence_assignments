import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import enum


# Enum representing the directions an ant can take.
class Direction(enum.Enum):
    east = 0
    north = 1
    west = 2
    south = 3

    # Direction to an int.
    # @param dir the direction.
    # @return an integer from 0-3.
    @classmethod
    def dir_to_int(cls, dir):
        return dir.value

    def opposite_direction(self):
        """
        Find the opposite direction of the given direction
        :return: the opposite direction of the given direction
        """
        return Direction((Direction.dir_to_int(self) + 2) % 4)
