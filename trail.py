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

        Doc:
        this removebranch function works by having the 4 if else statement to
        remove certain branch at different paths top and bottom

        complexity : O(1)
        """
        if isinstance(self.path_follow.store, TrailSeries):
            # return a new TrailSeries with the first mountain as the mountain attribute
            # and the rest of the TrailSeries as the following attribute
            return TrailSeries(self.path_follow.store.mountain, self.path_follow.store.following)
        if self.path_top.store is not None:
            return self.path_top.store
        elif self.path_bottom.store is not None:
            return self.path_bottom.store

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

        Doc: adds the mountain after the given mountain so it uses the self.mountain
        and then it updates into a new mountain
        """
        new_trail_series = TrailSeries(self.mountain, self.following)
        new_trail_series.mountain = mountain
        self.following = Trail(new_trail_series)
        return self




    def add_empty_branch_after(self) -> TrailStore:
        """Adds an empty branch after the current mountain, but before the following trail.


        Doc: this code have the first if statement to check if its none or not
        if it is it will update its trailsplit to None and return itself.
        The next elif is to check if the self.following is a instance of the
        tril series so it can be use into the trailsplit function at the final part
        lasty if nothing else then it will just take the trailseries and make it
        into a trail to use it into the trailsplit
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
        new_trail_series = Trail(TrailSeries(mountain, self))
        return new_trail_series

    def add_empty_branch_before(self) -> Trail:
        """Adds an empty branch before everything currently in the trail."""
        empty_trail_split = TrailSplit(Trail(None), Trail(None),Trail(self.store))
        return Trail(empty_trail_split)


    def follow_path(self, personality: WalkerPersonality) -> None:
        """Follow a path and add mountains according to a personality.

        Doc:
        For this follow path it is a bit tricky . To start of i decide to use a while loop to
        loop each trailsplit if there is one present . if there is then it will check with the
        given personality if it gives true or false . if its true then it will take the top
        path of the mountains , if its false then it will take the bottom path . After that
        it is a guarantee that when the top or bottom is taken there will always and must be a final\
        mountain so that will be taken no matter what path is choosen . After that , it will check if
        its a trailsplit or not if it is it will add the mountain base on the personality traits
        on how to add the mountain accordingly . next up for the bottom part this will check if its
        a trailseries or not . if it is it will add the mountain at the trailseries mountain part and then
        check the trailseries part to see if it is a trailsplit or not . if it is the trailsplit function will be
        run just like the top parh function where it will add the mountain base on the walker personality picking
        the top or bottom and then including the final . After the top path or bottom path is done it will add the
        final path mountain no matter what . After that it will loop again to check for a mountain before the
        mountain accesssing the paths before with that the path stores the current trail and run it back
        again at the top but it continues from where it left off

        time complexity: O(2^n) for the worst case as where the trail have two branches
        leading to a total of 2^n trails to go through

        best case willl be O(1) where just to have one trail in the case
        """
        current_trail = self
        while current_trail:
            if isinstance(current_trail.store, TrailSplit):
                # Call select_branch method from WalkerPersonality to decide which branch to take
                if personality.select_branch(current_trail.store.path_top, current_trail.store.path_bottom):
                    # Add a mountain to the trail based on the walker's personality
                    if isinstance(current_trail.store.path_top.store, TrailSplit):
                        if personality.select_branch(current_trail.store.path_top.store.path_top,
                                                     current_trail.store.path_top.store.path_bottom):
                            new_mountain = Mountain(current_trail.store.path_top.store.path_top.store.mountain.name,
                                                    current_trail.store.path_top.store.path_top.store.mountain.difficulty_level,
                                                    current_trail.store.path_top.store.path_top.store.mountain.length)
                            personality.add_mountain(new_mountain)
                        else:
                            new_mountain = Mountain(current_trail.store.path_top.store.path_bottom.store.mountain.name,
                                                    current_trail.store.path_top.store.path_bottom.store.mountain.difficulty_level,
                                                    current_trail.store.path_top.store.path_bottom.store.mountain.length)
                            personality.add_mountain(new_mountain)

                        if current_trail.store.path_top.store.path_follow.store:
                            new_mountain = Mountain(current_trail.store.path_top.store.path_follow.store.mountain.name,
                                                    current_trail.store.path_top.store.path_follow.store.mountain.difficulty_level,
                                                    current_trail.store.path_top.store.path_follow.store.mountain.length)
                            personality.add_mountain(new_mountain)


                    # always add the final mountain
                    if current_trail.store.path_follow.store:
                        new_mountain = Mountain(current_trail.store.path_follow.store.mountain.name,
                                                current_trail.store.path_follow.store.mountain.difficulty_level,
                                                current_trail.store.path_follow.store.mountain.length)
                        personality.add_mountain(new_mountain)


                    current_trail = current_trail.store.path_top.store.path_top



                else:
                    if isinstance(current_trail.store.path_bottom.store, TrailSeries):
                        new_mountain = Mountain(current_trail.store.path_bottom.store.mountain.name,
                                                current_trail.store.path_bottom.store.mountain.difficulty_level,
                                                current_trail.store.path_bottom.store.mountain.length)
                        personality.add_mountain(new_mountain)

                        if isinstance(current_trail.store.path_bottom.store.following.store,TrailSplit)\
                                and current_trail.store.path_bottom.store.following.store:

                            if personality.select_branch(current_trail.store.path_bottom.store.following.store.path_top,
                                                         current_trail.store.path_bottom.store.following.store.path_bottom):

                                if current_trail.store.path_bottom.store.following.store.path_top.store:
                                    new_mountain = Mountain(
                                        current_trail.store.path_bottom.store.following.store.path_top.store.mountain.name,
                                        current_trail.store.path_bottom.store.following.store.path_top.store.mountain.difficulty_level,
                                        current_trail.store.path_bottom.store.following.store.path_top.store.mountain.length)
                                    personality.add_mountain(new_mountain)

                            else:

                                if current_trail.store.path_bottom.store.following.store.path_bottom.store:
                                    new_mountain = Mountain(
                                        current_trail.store.path_bottom.store.following.store.path_bottom.store.mountain.name,
                                        current_trail.store.path_bottom.store.following.store.path_bottom.store.mountain.difficulty_level,
                                        current_trail.store.path_bottom.store.following.store.path_bottom.store.mountain.length)
                                    personality.add_mountain(new_mountain)


                            if current_trail.store.path_bottom.store.following.store.path_follow.store:
                                new_mountain = Mountain(
                                    current_trail.store.path_bottom.store.following.store.path_follow.store.mountain.name,
                                    current_trail.store.path_bottom.store.following.store.path_follow.store.mountain.difficulty_level,
                                    current_trail.store.path_bottom.store.following.store.path_follow.store.mountain.length)
                                personality.add_mountain(new_mountain)

                    # always add the final mountain
                    if current_trail.store.path_follow.store:
                        new_mountain = Mountain(current_trail.store.path_follow.store.mountain.name,
                                                current_trail.store.path_follow.store.mountain.difficulty_level,
                                                current_trail.store.path_follow.store.mountain.length)
                        personality.add_mountain(new_mountain)

                    current_trail = current_trail.store.path_bottom

                    #else:
                       #current_trail = None
            else:
                current_trail = None




    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        mountains = []
        stack = [self]
        while stack:
            current_trail = stack.pop()
            if isinstance(current_trail.store, TrailSeries):
                mountains.append(current_trail.store.mountain)
                if current_trail.store.following:
                    stack.append(current_trail.store.following)
            elif isinstance(current_trail.store, TrailSplit):
                if current_trail.store.path_top:
                    stack.append(current_trail.store.path_top)
                if current_trail.store.path_bottom:
                    stack.append(current_trail.store.path_bottom)
                if current_trail.store.path_follow:
                    stack.append(current_trail.store.path_follow)
        return mountains


    def length_k_paths(self, k) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        """
        Returns a list of all paths of containing exactly k mountains.
        Paths are represented as lists of mountains.

        Paths are unique if they take a different branch, even if this results in the same set of mountains.
        """
        paths = []
        stack = [(self, [])]
        while stack:
            current_trail, current_path = stack.pop()
            if isinstance(current_trail.store, TrailSeries):
                current_path.append(current_trail.store.mountain)
                if len(current_path) == k:
                    paths.append(current_path)
                elif current_trail.store.following:
                    stack.append((current_trail.store.following, current_path.copy()))
            elif isinstance(current_trail.store, TrailSplit):
                if current_trail.store.path_top:
                    stack.append((current_trail.store.path_top, current_path.copy()))
                if current_trail.store.path_bottom:
                    stack.append((current_trail.store.path_bottom, current_path.copy()))
                if current_trail.store.path_follow:
                    stack.append((current_trail.store.path_follow, current_path.copy()))
        return paths
