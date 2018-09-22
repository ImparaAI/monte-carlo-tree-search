import random
from math import log, sqrt

class Node:

	def __init__(self, state):
		self.state = state
		self.win_value = 0
		self.policy_value = None
		self.visits = 0
		self.parent = None
		self.children = []
		self.expanded = False
		self.player_number = None

	def update_win_value(self, value):
		self.win_value += value
		self.visits += 1

		if self.parent:
			self.parent.update_win_value(value)

	def update_policy_value(self, value):
		self.policy_value = value

	def add_child(self, child):
		self.children.append(child)
		child.parent = self

	def add_children(self, children):
		for child in children:
			self.add_child(child)

	def get_preferred_child(self, root_node):
		best_children = []
		best_score = float('-inf')

		for child in self.children:
			score = child.get_score(root_node)

			if score > best_score:
				best_score = score
				best_children = [child]
			elif score == best_score:
				best_children.append(child)

		return random.choice(best_children)

	def get_score(self, root_node):
		discovery_constant = 0.35
		discovery_operand = discovery_constant * (self.policy_value or 1) * sqrt(log(self.parent.visits) / (self.visits or 1))

		win_multiplier = 1 if self.parent.player_number == root_node.player_number else -1
		win_operand = win_multiplier * self.win_value / (self.visits or 1)

		self.score = win_operand + discovery_operand

		return self.score

	def is_scorable(self):
		return self.visits or self.policy_value != None