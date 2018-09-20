A Python3 library that you can use to run a Monte Carlo tree search, either traditionally with drilling down to end game states or with expert policies as you might provide from a neural network.

- **Version:** 1.1.2

[![Build Status](https://travis-ci.org/ImparaAI/monte-carlo-tree-search.png?branch=master)](https://travis-ci.org/ImparaAI/monte-carlo-tree-search)

# Basics

If you're unfamiliar with the Monte Carlo tree search algorithm, you should first become familiar with it. Simply put, it helps make a decision from a set of possibile options by doing one of two things:

- Constructing likely outcomes either by drilling down into random endstates for each option or..
- Using expert policies to make similar determinations without having to drill down to end states

As the user of this library, you only have to provide a function that finds the direct children of each node, and optionally a function for evaluating nodes for end state outcomes.

# Usage

Create a new Monte Carlo tree:

```python
from game import Game
from montecarlo.node import Node
from montecarlo.montecarlo import MonteCarlo

montecarlo = MonteCarlo(Node(Game()))
```

When instantiating the `MonteCarlo` class, you must pass in the root node of the tree with its state defined. The state of the node can be anything you will need to determine what the children of that node will be.

For the sake of demonstration, we will assume you have an generic `Game` library that can tell you what moves are possible and make those moves.

## Traditional Monte Carlo

Add a child finder and a node evaluator:

```python
def child_finder(node):
	for move in node.state.get_possible_moves():
		child = Node(deepcopy(node.state)) #or however you want to construct the child's state
		child.state.move(move) #or however your library works
		node.add_child(child)

def node_evaluator(self, node):
	if node.state.won():
		return 1
	elif node.state.lost():
		return -1

montecarlo.child_finder = child_finder
montecarlo.node_evaluator = node_evaluator
```

The `child_finder` simply needs to add new child nodes to the parent node passed into the function. If there are no children, the library won't try to drill down further. In that scenario, however, the parent should be in an end state, so the `node_evaluator` should return a value between `-1` and `1`.

## Expert policy (AI)

If you have an expert policy that you can apply to the children as they're being generated, the library will recognize that it doesn't need to make the costly drill down to an end state. If your neural net produces both an expert policy value for the children and a win value for the parent node, you can skip declaring the `node_evaluator` altogether.

```python
def child_finder(self, node):
	win_value, expert_policy_values = neural_network.predict(node.state)

	for move in node.state.get_possible_moves():
		child = Node(deepcopy(node.state))
		child.state.move(move)
		child.policy_value = get_child_policy_value(child, expert_policy_values) #should return a value between 0 and 1
		node.add_child(child)

	node.update_win_value(win_value)

montecarlo.child_finder = child_finder
```

## Simulate and make a choice

Run the simulations:

```python
montecarlo.simulate(50) #number of expansions to run. higher is typically more accurate at the cost of processing time
```

Once the simulations have been run you can ask the instance to make a choice:

```python
chosen_child_node = montecarlo.make_choice()
chosen_child_node.state.do_something()
```

After you've chosen a new root node, you can override it on the `montecarlo` instance and do more simulations from the new position in the tree.

```python
montecarlo.root_node = montecarlo.make_choice()
```