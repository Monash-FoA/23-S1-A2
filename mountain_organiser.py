from __future__ import annotations

from typing import TypeVar
from mountain import Mountain
#from algorithms.binary_search import binary_search,_binary_search_aux


T = TypeVar("T")
class MountainOrganiser:

    def __init__(self) -> None:
        self.mountains = []

    def cur_position(self, mountain: Mountain) -> int:
        lo, hi = 0, len(self.mountains) - 1
        while lo <= hi:
            mid = lo + (hi - lo) // 2
            if self.mountains[mid] == mountain:
                return mid
            elif self.mountains[mid].length < mountain.length or (
                    self.mountains[mid].length == mountain.length and self.mountains[mid].name < mountain.name):
                lo = mid + 1
            else:
                hi = mid - 1
        raise KeyError("Mountain not found")

    def add_mountains(self, mountains: list[Mountain]) -> None:
        self.mountains.extend(mountains)
        self.mountains.sort(key=lambda m: (m.length,m.name))




