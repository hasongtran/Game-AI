import json
from heapq import heappop, heappush
from collections import namedtuple, defaultdict, OrderedDict
from timeit import default_timer as time
from math import inf

Recipe = namedtuple('Recipe', ['name', 'check', 'effect', 'cost'])

with open('Crafting.json') as f:
    Crafting = json.load(f)

class State(OrderedDict):
    """ This class is a thin wrapper around an OrderedDict, which is simply a dictionary which keeps the order in
        which elements are added (for consistent key-value pair comparisons). Here, we have provided functionality
        for hashing, should you need to use a state as a key in another dictionary, e.g. distance[state] = 5. By
        default, dictionaries are not hashable. Additionally, when the state is converted to a string, it removes
        all items with quantity 0.

        Use of this state representation is optional, should you prefer another.
    """

    def __key(self):
        return tuple(self.items())

    def __hash__(self):
        return hash(self.__key())

    def __lt__(self, other):
        return self.__key() < other.__key()

    def copy(self):
        new_state = State()
        new_state.update(self)
        return new_state

    def __str__(self):
        return str(dict(item for item in self.items() if item[1] > 0))


def make_checker(rule):
    # Implement a function that returns a function to determine whether a state meets a
    # rule's requirements. This code runs once, when the rules are constructed before
    # the search is attempted.

    # check for Requires or Consumes, then check if in required_items

    required_items = {}
    if 'Requires' in rule:
        for item, required in rule['Requires'].items():
            if required:
                if item not in required_items:
                    required_items[item] = 1
    if 'Consumes' in rule:
        for item, amount in rule['Consumes'].items():
            if item not in required_items:
                required_items[item] = amount

    def check(state):
        # This code is called by graph(state) and runs millions of times.
        # Tip: Do something with rule['Consumes'] and rule['Requires'].

        for item, amount in required_items.items():
            if not state[item] or state[item] < amount:
                return False
        return True

    return check



def make_effector(rule):
    # Implement a function that returns a function which transitions from state to
    # new_state given the rule. This code runs once, when the rules are constructed
    # before the search is attempted.

    def effect(state):
        # This code is called by graph(state) and runs millions of times
        # Tip: Do something with rule['Produces'] and rule['Consumes'].

        next_state = state.copy()
        if 'Consumes' in rule:
            for item, amount in rule['Consumes'].items():
                next_state[item] -= amount
        if 'Produces' in rule:
            for item, amount in rule['Produces'].items():
                if item not in next_state:
                    next_state[item] = amount
                else: 
                    next_state[item] += amount

        return next_state

    return effect


def make_goal_checker(goal):
    # Implement a function that returns a function which checks if the state has
    # met the goal criteria. This code runs once, before the search is attempted.

    def is_goal(state):
        # This code is used in the search process and may be called millions of times.
        for item, amount in goal.items():
            if state[item] < amount:
                return False

        return True

    return is_goal


def graph(state):
    # Iterates through all recipes/rules, checking which are valid in the given state.
    # If a rule is valid, it returns the rule's name, the resulting state after application
    # to the given state, and the cost for the rule.
    for r in all_recipes:
        if r.check(state):
            yield (r.name, r.effect(state), r.cost)


def heuristic(state, action):
    # tools = ['bench', 'furnace','iron_axe', 'iron_pickaxe', 'stone_axe', 'stone_pickaxe', 'wooden_axe', 'wooden_pickaxe']
    # Crafting['Items'] = tools
    # curr_state = state.copy
    # # goal = Crafting["Goals"]
    #
    # # if there already exist 1 tool, don't try to make any more
    # for item in tools:
    #     if curr_state[item] > 1:
    #         return inf
    #     elif item in action:
    #         return 0
    #
    # if state['iron_axe'] == 1:
    #     if 'stone_axe' and 'wooden_axe' in action:
    #         return inf
    # elif state['stone_axe'] == 1:
    #     if 'wooden_axe' and 'iron_axe' in action:
    #         return inf
    # elif state['wooden_axe'] == 1:
    #     if 'stone_axe' and 'iron_axe' in action:
    #         return inf
    #
    # if state['iron_pickaxe'] == 1:
    #     if 'stone_pickaxe' and 'wooden_pickaxe' in action:
    #         return inf
    # elif state['stone_pickaxe'] == 1:
    #     if 'iron_pickaxe' and 'wooden_pickaxe' in action:
    #         return inf
    # elif state['wooden_pickaxe'] == 1:
    #     if 'iron_pickaxe' and 'stone_pickaxe' in action:
    #         return inf

    pass


def search(graph, state, is_goal, limit, heuristic):

    # Implement your search here! Use your heuristic here!
    # When you find a path to the goal return a list of tuples [(state, action)]
    # representing the path. Each element (tuple) of the list represents a state
    # in the path and the action that took you to this state

    start_time = time()
    queue = [(0, state)]
    start = state
    dist = {}
    dist[start] = None
    action = {}
    action[start] = None
    parent = {}
    parent[start] = None


    while time() - start_time < limit and queue:
        curr_cost, curr_node = heappop(queue)

        if is_goal(curr_node):
            plan = []
            while curr_node is not None:
                plan.append((curr_node, action[curr_node]))
                curr_node = parent[curr_node]
            plan.reverse()
            print("Search Time: ", time() - start_time, '\n')
            #print(plan)
            return plan

        else:
            for next_state in graph(curr_node):
                name, neighbor, cost = next_state
                curr_dist =  curr_cost + cost
                # if distance[neighbor] DNE or the new distance is less than old distance
                if (neighbor not in dist) or curr_dist < dist[neighbor]:
                    action[neighbor] = name
                    parent[neighbor] = curr_node
                    dist[neighbor] = curr_dist
                    # heappush(queue, (curr_dist + heuristic(neighbor, name), neighbor))
                    heappush(queue, (curr_dist, neighbor))


    print(time() - start_time, 'seconds.')
    print("Failed to find a path from", state, 'within time limit.')


if __name__ == '__main__':
    with open('Crafting.json') as f:
        Crafting = json.load(f)

    # List of items that can be in your inventory:
    print('\n', 'All items:', Crafting['Items'], '\n')

    # List of items in your initial inventory with amounts:
    print('Initial inventory:', Crafting['Initial'], '\n')

    # List of items needed to be in your inventory at the end of the plan:
    print('Goal:',Crafting['Goal'],'\n')

    # Dict of crafting recipes (each is a dict):
    #print('Example recipe:','craft stone_pickaxe at bench ->',Crafting['Recipes']['craft stone_pickaxe at bench'])

    #Build rules
    all_recipes = []
    for name, rule in Crafting['Recipes'].items():
        # print("Name and rules:", name, rule)
        checker = make_checker(rule)
        effector = make_effector(rule)
        recipe = Recipe(name, checker, effector, rule['Time'])
        all_recipes.append(recipe)

    # Create a function which checks for the goal
    is_goal = make_goal_checker(Crafting['Goal'])

    # Initialize first state from initial inventory
    state = State({key: 0 for key in Crafting['Items']})
    state.update(Crafting['Initial'])

    # Search for a solution
    resulting_plan = search(graph, state, is_goal, 30, heuristic)

    if resulting_plan:
        cost = 0
        len = -1
        # Print resulting plan
        for state, action in resulting_plan:
            for item in all_recipes:
                if item.name is action:
                    cost += item.cost
            len += 1
            print(cost, ", ", action,", ", state, '\n')
        print("Cost:", cost, ", Length:", len)
