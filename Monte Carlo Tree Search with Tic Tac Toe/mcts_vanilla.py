from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 1000
explore_faction = 2.


def traverse_nodes(node, board, state, identity):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    """
    
    #copy parameters
    curr_state = state
    curr_node = node
    
    #while selected node doesnt have children or the current state game has ended
    while not curr_node.untried_actions and not board.is_ended(curr_state):
        
        node_list = []
        UCB_list = []
        
        #for possible child nodes of current node
        for i in curr_node.child_nodes:
            temp = curr_node.child_nodes[i]
            
            #dont divide by 0
            if temp.visits != 0:
                UCB = ((temp.wins / temp.visits) + (explore_faction * sqrt(2*log(curr_node.visits / temp.visits))))
    
                # if the current player is identity, curr node's UCB is enemy's
                if board.current_player == identity:
                    UCB = (1 - ( temp.wins / temp.visits) + (explore_faction * sqrt(2*log(curr_node.visits / temp.visits))))
            else:
                UCB = 0
            
            #if the UCB values is the greatest, add to front, else append to end
            if node_list and UCB_list[0] < UCB:
                UCB_list.insert(0, UCB)
                node_list.insert(0, temp)
            else:
                UCB_list.append(UCB)
                node_list.append(temp)
        
        #if no children
        if not node_list:
            return curr_node
        
        #if children
        if node_list:
            curr_node = node_list[0]
            curr_state = board.next_state(curr_state, curr_node.parent_action)
    
    return curr_node
    # pass
    # Hint: return leaf_node


# only called when there is an untried action
def expand_leaf(node, board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node.

    """
    # select random untried action
    selected_action = choice(node.untried_actions)
    node.untried_actions.remove(selected_action)

    # run selected action and get new state
    new_state = board.next_state(state, selected_action)
    # create new node from new action and state
    new_node = MCTSNode(parent=node, parent_action=selected_action, action_list=board.legal_actions(new_state))
    # update current node
    node.child_nodes[selected_action] = new_node

    return new_node

    # pass
    # Hint: return new_node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    # run until game ended
    rollout_state = state
    while 1:
        if board.is_ended(rollout_state):
            break
        rollout_move = choice(board.legal_actions(rollout_state))
        rollout_state = board.next_state(rollout_state, rollout_move)

    # check winner and return
    # return winner, on tie return 0
    win_dict = board.points_values(rollout_state)
    if win_dict[1] == -1:
        return 2
    elif win_dict[1] == 1:
        return 1
    else:
        return 0

        # return winner
        # pass


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    # where if curr player wins, won = 1
    #we iterate every other node so that the correct player win count
    #is incremented
    while 1:
        node.visits += 1
        count = 0
        if won == 1 and count % 2 == 0:
            node.wins += 1
        elif won == 0 and count % 2 == 1:
            node.wins += 1

        count += 1

        if node.parent == None:
            break
        else:
            node = node.parent

    pass


def think(board, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))

    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node

        # Do MCTS - This is all you!
        selected_node = traverse_nodes(node, board, sampled_game, identity_of_bot)

        # no more possible exploration
        if not selected_node.untried_actions:
            continue
        
        #get proper state
        action_list = []
        temp_node = selected_node.parent
        while temp_node != None:
            action_list.append(temp_node.parent_action)
            temp_node = temp_node.parent
        #reverse list
        action_list.reverse()
        
        #apply actions to get appropriate state
        selected_state = sampled_game
        while action_list:
            curr_action = action_list.pop(0)
            if curr_action == None:
                continue
            selected_state = board.next_state(selected_state, curr_action)
        
        #expansion
        new_node = expand_leaf(selected_node, board, selected_state)
        new_state = board.next_state(selected_state, new_node.parent_action)
        
        #rollout
        roll_winner = rollout(board, new_state)
        
        #backpropagate
        if roll_winner == 0:
            backpropagate(new_node, -1)
        elif roll_winner != board.current_player(new_state):
            backpropagate(new_node, 1)
        else:
            backpropagate(new_node, 0)

    
    # select highest UCB node or winning node
    node = root_node
    curr_state = state
    node_list = []
    rate_list = []
    
    #select best UCB
    for i in node.child_nodes:
        temp = node.child_nodes[i]
        
        #check for win
        new_state = board.next_state(curr_state, temp.parent_action)
        if board.is_ended(new_state) and board.points_values(new_state)[identity_of_bot] == 1:
            return temp.parent_action
        
        if temp.visits != 0:
            rate = (temp.wins / temp.visits)
        else:
            rate = 0
            
        if node_list and rate_list[0] < rate:
            rate_list.insert(0, rate)
            node_list.insert(0, temp)
        else:
            rate_list.append(rate)
            node_list.append(temp)

    return node_list[0].parent_action
    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    # return None
