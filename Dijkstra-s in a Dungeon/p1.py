#partner: Jason Ting


from p1_support import load_level, show_level, save_level_costs
from math import inf, sqrt
from heapq import heappop, heappush


def dijkstras_shortest_path(initial_position, destination, graph, adj):
    """ Searches for a minimal cost path through a graph using Dijkstra's algorithm.

    Args:
        initial_position: The initial cell from which the path extends.
        destination: The end location for the path.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        If a path exits, return a list containing all cells from initial_position to destination.
        Otherwise, return None.

    """
    dist = {}  # Total distance to reach
    prev = {}  # The previous node
    queue = []  # Empty stack
    dist[initial_position] = 0
    prev[initial_position] = None
    heappush(queue, (0, initial_position))  # push initial position on the queue
    # while there is something in the queue
    while (queue):
        distance, cur_node = heappop(queue)
        #If you reached the destination break out of the loop
        if cur_node == destination:

            print("Here")
            break

        # print("\n Current Node & distance:", cur_node, distance)
        # print("\nQueue:", queue)
        # Find all adjacent nodes
        next = adj(graph, cur_node)
        # print("\n next value:", next)
        for value, neighbor in next:
            totCost = distance + value
            # Check the cost of going to the node
            if neighbor not in dist or dist[neighbor] > totCost:
                dist[neighbor] = totCost
                prev[neighbor] = cur_node
                heappush(queue, (totCost, neighbor))

    paths = []
    # print("\nSource:", initial_position)
    # print("\nprev: ",prev)
    # print("\n destination:", destination)
    if(cur_node == destination):

        while(cur_node != None):
            paths.append(cur_node)
            cur_node = prev[cur_node]


        #Flip it around so it's going from source to destination
        paths.reverse()
    # print("\n path:", paths)

    return paths



def dijkstras_shortest_path_to_all(initial_position, graph, adj):
    """ Calculates the minimum cost to every reachable cell in a graph from the initial_position.

    Args:
        initial_position: The initial cell from which the path extends.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        A dictionary, mapping destination cells to the cost of a path from the initial_position.
    """

    dist = {}       #Total distance to reach
    queue = []      #Empty stack
    dist[initial_position] = 0

    heappush(queue, (0, initial_position))  # push initial position on the queue
    #while there is something in the queue
    while (queue):
        distance, cur_node = heappop(queue)
        # print("\n Current Node & distance:", cur_node, distance)
        # print("\nQueue:", queue)
        #Find all adjacent nodes
        next = adj(graph, cur_node)
        #print("\n next value:", next)
        for value, neighbor in next:
                totCost = distance + value
                #Check the cost of going to the node
                if (neighbor not in dist or dist[neighbor] > totCost):

                    dist[neighbor] = totCost
                    heappush(queue, (totCost, neighbor))

    # print("\n dist:", dist)
    return dist


def navigation_edges(level, cell):
    """ Provides a list of adjacent cells and their respective costs from the given cell.

    Args:
        level: A loaded level, containing walls, spaces, and waypoints.
        cell: A target location.

    Returns:
        A list of tuples containing an adjacent cell's coordinates and the cost of the edge joining it and the
        originating cell.

        E.g. from (0,0):
            [((0,1), 1),
             ((1,0), 1),
             ((1,1), 1.4142135623730951),
             ... ]
    """
    all_cells = []
    x, y = cell
    # visit all adjacent cells
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            next_x = x + dx
            next_y = y + dy
            next = (next_x, next_y)

            #calc distance from cell to cell
            cost = sqrt(dx * dx + dy * dy)
            #add distances to the list of all cells
            if cost > 0 and next in level['spaces']:
                all_cells.append((cost, next))
    return all_cells


def test_route(filename, src_waypoint, dst_waypoint):
    """ Loads a level, searches for a path between the given waypoints, and displays the result.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        dst_waypoint: The character associated with the destination waypoint.

    """

    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source and destination coordinates from the level.
    src = level['waypoints'][src_waypoint]
    dst = level['waypoints'][dst_waypoint]

    # Search for and display the path from src to dst.
    path = dijkstras_shortest_path(src, dst, level, navigation_edges)
    if path:
        show_level(level, path)
    else:
        print("No path possible!")


def cost_to_all_cells(filename, src_waypoint, output_filename):
    """ Loads a level, calculates the cost to all reachable cells from 
    src_waypoint, then saves the result in a csv file with name output_filename.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        output_filename: The filename for the output csv file.

    """
    
    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source coordinates from the level.
    src = level['waypoints'][src_waypoint]
    
    # Calculate the cost to all reachable cells from src and save to a csv file.
    costs_to_all_cells = dijkstras_shortest_path_to_all(src, level, navigation_edges)
    save_level_costs(level, costs_to_all_cells, output_filename)


if __name__ == '__main__':
    filename, src_waypoint, dst_waypoint = 'my_maze.txt', 'a','d'

    # Use this function call to find the route between two waypoints.
    test_route(filename, src_waypoint, dst_waypoint)

    # Use this function to calculate the cost to all reachable cells from an origin point.
    cost_to_all_cells(filename, src_waypoint, 'my_maze_costs.csv')
