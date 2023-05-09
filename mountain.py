from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Mountain:

    name: str
    difficulty_level: int
    length: int

    def __lt__(self, other: 'Mountain') -> bool:
        if self.difficulty_level < other.difficulty_level:
            return True
        elif self.difficulty_level > other.difficulty_level:
            return False
        else:
            return self.length < other.length