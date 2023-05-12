from __future__ import annotations

from typing import TypeVar
from mountain import Mountain
#from algorithms.binary_search import binary_search,_binary_search_aux


T = TypeVar("T")
class MountainOrganiser:

    def __init__(self) -> None:
        """
        set the mountin into empty list
        """
        self.mountains = []

    def cur_position(self, mountain: Mountain) -> int:
        """
        This code takes the method of using binary search to
        find the index of the mountain . it have two pointers hi and low
        which will be the lower and the upper bound of the search range .
        first it enters the while loop that continues as long as the low
        is leeser than the hi . it then  calculates the midpoint index mid
        and checks if the mountain at that index is equal to the input mountain
        if it is then it return the mid index if not it continues to check if
        the length and name of the mountain at index mid with those of the input
        mountain. If the length is less than that of the input mountain, or if the
        lengths are equal but the name of the mountain at mid is less than that of
        the input mountain, then the search range is narrowed to the upper half of
        the current range by setting low to mid + 1


        time complexity:

        good :O(log n) - when the list is sorted and the search is successful,
        the function will find the mountain in the list in logarithmic time

        bad :O(log n) when the list is sorted and the search is unsuccessful, the function
        will iterate through the list using binary search, so the time complexity is also logarithmic.
        """
        low, hi = 0, len(self.mountains) - 1
        while low <= hi:
            mid = low + (hi - low) // 2
            if self.mountains[mid] == mountain:
                return mid
            elif self.mountains[mid].length < mountain.length or (
                    self.mountains[mid].length == mountain.length and self.mountains[mid].name < mountain.name):
                low = mid + 1
            else:
                hi = mid - 1
        raise KeyError("Mountain not found")

    def add_mountains(self, mountains: list[Mountain]) -> None:
        """
        add the mountain to the alreaddy list using extend and then sort it
        by its length and the name

        time complexity will be

        good : O(n log n) where n is the total number of mountains
        (size of the self.mountains list). This is because it uses the
        built-in sort method, which has a worst-case time complexity of O(n log n)

        bad: O(n log n) also it also sorts at the same time as in good as n is
        also the total number of mountains(size of the self.mountains list) only when
        the array is already sorted or nearly sorted it will have O(n)
        """
        self.mountains.extend(mountains) # using extend mountain to combine the list
        self.mountains.sort(key=lambda m: (m.length,m.name))




