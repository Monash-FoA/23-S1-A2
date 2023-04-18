from __future__ import annotations
from dataclasses import dataclass
from data_structures.linked_stack import LinkedStack



from mountain import Mountain
from typing import TYPE_CHECKING, Union

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from personality import WalkerPersonality
    from personality import TopWalker
    from personality import BottomWalker
    from personality import LazyWalker





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
        """Removes the branch, should just leave the remaining following trail."""
        #return self.path_follow.store
        next_trail = Trail(None)
        return TrailSeries(self.path_follow.store.mountain, next_trail)


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
        #next_trail = Trail(None)
        return TrailSeries(None, self.following)


       

    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain in series before the current one."""
                
        #following_store_trail = Trail(TrailSeries(self.mountain, Trail(self.following.store)))

        following_store_trail = Trail(TrailSeries(self.mountain, self.following))
        return TrailSeries(mountain, following_store_trail)


        
    def add_empty_branch_before(self) -> TrailStore:
        """Adds an empty branch, where the current trailstore is now the following path."""
       #new_store = TrailSplit(None, None, self)
        #return Trail(new_store)
        return TrailSplit(Trail(None), Trail(None), Trail(TrailSeries(self.mountain,self.following)))

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain after the current mountain, but before the following trail."""
        new_following_trail = TrailSeries(mountain, self.following)
        return TrailSeries(self.mountain, Trail(new_following_trail))
        
        

    def add_empty_branch_after(self) -> TrailStore:
        """Adds an empty branch after the current mountain, but before the following trail."""
        new_following_trail = TrailSplit(Trail(None), Trail(None), self.following)
        return TrailSeries(self.mountain, Trail(new_following_trail))
       

TrailStore = Union[TrailSplit, TrailSeries, None]


@dataclass
class Trail:
    store: TrailStore = None

    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """Adds a mountain before everything currently in the trail."""
        return Trail(TrailSeries(mountain, self))

    def add_empty_branch_before(self) -> Trail:
        """Adds an empty branch before everything currently in the trail."""
        
        return Trail(TrailSplit(Trail(None), Trail(None), self))
    
    
    def follow_path(self, personality: WalkerPersonality) -> None:
        """Follow a path and add mountains according to a personality."""
        stack = LinkedStack()
        #stack.push(self)
        while self.store is not None:
            if self.__class__.__name__ == "TrailSplit":
                if personality.select_branch(Trail(self.store.path_top.store),Trail(self.store.path_bottom.store) ) is True:
                    personality.add_mountain(self.store.path_top.store.mountain)
                    stack.push(self.store.path_top.store)
                elif personality.select_branch(Trail(self.store.path_top.store),Trail(self.store.path_bottom.store)) is False:
                    personality.add_mountain(self.store.path_bottom.store.mountain)
                    stack.push(self.store.path_bottom.store)
                elif personality.__class__.__name__ == "LazyWalker":
                    if personality.select_branch(Trail(self.store.path_top.store),Trail(self.store.path_bottom.store)):
                        stack.push(self.store.path_top.store)
                    else:
                        stack.push(self.store.path_bottom.store)
            elif self.__class__.__name__ == "TrailSeries":
                personality.add_mountain(self.store.mountain)
                


    
    





       # while not stack.is_empty():
            # current = stack.pop()
             

        #     if current.__class__.__name__ == "TrailSplit":
        #         if personality.__class__.__name__ == "TopWalker":
        #             stack.push(current.top_trail.store)
        #         elif personality.__class__.__name__ == "BottomWalker":
        #             stack.push(current.bottom_trail.store)
        #         elif personality.__class__.__name__ == "LazyWalker":
        #             if personality.select_branch(current.top_trail, current.bottom_trail):
        #                 stack.push(current.top_trail.store)
        #             else:
        #                 stack.push(current.bottom_trail.store)
                
        #     elif current.__class__.__name__ == "TrailSeries":
        #         personality.add_mountain(current.mountain)
        #         if current.next_trail is not None:
        #             stack.push(current.next_trail.store)

    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        raise NotImplementedError() 

    def length_k_paths(self, k) -> list[list[Mountain]]:
        """
        Returns a list of all paths of containing exactly k mountains.
        Paths are represented as lists of mountains.

        Paths are unique if they take a different branch, even if this results in the same set of mountains.
        """
        raise NotImplementedError()
