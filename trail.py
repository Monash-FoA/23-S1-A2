from __future__ import annotations
from dataclasses import dataclass

from mountain import Mountain

from typing import TYPE_CHECKING, Union

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from personality import WalkerPersonality

@dataclass
class TrailSplit:
    """
    A split in the trail.
       ___path_top____
      /               \
    -<                 >-path_follow-
      \__path_bottom__/
    """

    path_top: Trail
    path_bottom: Trail
    path_follow: Trail

    def remove_branch(self) -> TrailStore:
        """Removes the branch, should just leave the remaining following trail.
        """
        if isinstance(self.path_follow.store, TrailSeries):
            # return a new TrailSeries with the first mountain as the mountain attribute
            # and the rest of the TrailSeries as the following attribute
            return TrailSeries(self.path_follow.store.mountain, self.path_follow.store.following)
        if self.path_top.store is not None:
            return self.path_top.store
        elif self.path_bottom.store is not None:
            return self.path_bottom.store
        #elif self.path_follow.store is not None:
            #return self.path_follow.store
        else:
            raise ValueError("No branch to remove.")

@dataclass
class TrailSeries:
    """
    A mountain, followed by the rest of the trail

    --mountain--following--

    """

    mountain: Mountain
    following: Trail

    def remove_mountain(self) -> TrailStore:
        """Removes the mountain at the beginning of this series."""
        self.mountain = None
        return self.following.store

    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain in series before the current one.

        """
        new_trail_series = TrailSeries(mountain, self.following)
        self.following.store = self
        return new_trail_series

    def add_empty_branch_before(self) -> TrailStore:
        """Adds an empty branch, where the current trailstore is now the following path."""
        empty_trail_split = TrailSplit(Trail(None), Trail(None), Trail(TrailSeries(self.mountain,self.following)))
        self.following.store = empty_trail_split
        return empty_trail_split

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """

        Adds a mountain after the current mountain, but before the following trail.

        """
        new_trail_series = TrailSeries(self.mountain, self.following)
        new_trail_series.mountain = mountain
        self.following = Trail(new_trail_series)
        return self




    def add_empty_branch_after(self) -> TrailStore:
        """Adds an empty branch after the current mountain, but before the following trail.

        """


        if self.following.store == TrailSeries(self.mountain,self.following):
            empty_trail_split = TrailSplit(Trail(None), Trail(None), Trail(None))
            self.following.store = empty_trail_split
            return self
        elif isinstance(self.following.store, TrailSeries):
            empty_trail_split = TrailSplit(Trail(None), Trail(None), Trail(self.following.store))
            self.following.store = empty_trail_split
            return self
        empty_trail_split = TrailSplit(Trail(None), Trail(None), Trail(TrailSeries(self.mountain, self.following)))
        self.following.store = empty_trail_split
        return self








TrailStore = Union[TrailSplit, TrailSeries, None]

@dataclass
class Trail:

    store: TrailStore = None

    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """Adds a mountain before everything currently in the trail."""
        new_trail_series = TrailSeries(mountain, self.store)
        self.store = new_trail_series
        return new_trail_series

    def add_empty_branch_before(self) -> Trail:
        """Adds an empty branch before everything currently in the trail."""
        empty_trail_split = TrailSplit(Trail(None), Trail(None),Trail(self.store))
        return Trail(empty_trail_split)


    def follow_path(self, personality: WalkerPersonality) -> None:
        """Follow a path and add mountains according to a personality."""
        current_trail = self
        while current_trail.store is not None:
            if isinstance(current_trail.store, TrailSeries):
                # Call select_branch method from WalkerPersonality to decide which branch to take
                if personality.select_branch(current_trail.store.mountain, current_trail.store.following.mountain):
                    # Add a mountain to the trail based on the walker's personality
                    new_mountain = Mountain(personality.get_next_mountain_height())
                    current_trail = current_trail.store.add_mountain_before(new_mountain)
                else:
                    current_trail = current_trail.store.following
            elif isinstance(current_trail.store, TrailSplit):
                # Call select_branch method from WalkerPersonality to decide which branch to take
                if personality.select_branch(current_trail.store.path_top.mountain,
                                             current_trail.store.path_bottom.mountain):
                    current_trail = current_trail.store.path_top
                else:
                    current_trail = current_trail.store.path_bottom
            else:
                raise ValueError("Invalid TrailStore type.")
    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        raise NotImplementedError()

    def length_k_paths(self, k) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        """
        Returns a list of all paths of containing exactly k mountains.
        Paths are represented as lists of mountains.

        Paths are unique if they take a different branch, even if this results in the same set of mountains.
        """
        raise NotImplementedError()
