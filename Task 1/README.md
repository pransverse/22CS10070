# VizDoom (Level 1)

This project consists of two parts:
- Global Planning
- Trajectory Following

## Global Planning

This section consists of finding a path from the _white_ starting point to the _blue_ end point using informed rrt* algorithm, after generating a ``map.png`` from the automap buffer.
Further the path obtained through rrt is run through the fucntion ``avoid_walls`` to smooth out the path. This implementation can be found in the file ``Task 1\examples\python\rrtstar.py``. This path is saved as ``path.npz`` and also as an image ``path.png``. The original path before applying ``avoid_walls`` is saved as ``orig_path.png``.

#### Informed RRT-star algorithm:
This is a variation of RRT star in which the goal coordinates is known prior to path finding and is used to guide the random exploration making it faster and more effective. RRT star itself is a variation of the RRT algorithm that combines RRT with a cost heuristic function. After the addition of every node, the most cost effective path to the node is chosen from among its nearest neighbours. 


## Trajectory Following

This section of consists of mapping the map coordinates to the game world coordinates and then navigating the path in the previous section using game controls. For the mapping, I used linear regression after generating multiple points across the game and finding their corresponding map coordinates (implemented using function ``map_to_game``). The player moves from one point of the path to the other using the ``navigate`` function. This function first turns by whatever angle is required and then moves towards the target point until it reaches within a particular radius. 

For error handling, anytime the target moves in the same direction for more than the distance between the two points, the loop ends and the player _randomly_ moves either towards the next point or the previous point. 

Implementation in ``Task 1\examples\python\level_1.py``

Recording of Level 1: <https://clipchamp.com/watch/vcBgBRzlBfv>
