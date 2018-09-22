from random import choice

class MonteCarlo:

	def __init__(self, root_node):
		self.root_node = root_node
		self.child_finder = None
		self.node_evaluator = lambda child, montecarlo: None

	def make_choice(self):
		best_children = []
		most_visits = float('-inf')

		for child in self.root_node.children:
			if child.visits > most_visits:
				most_visits = child.visits
				best_children = [child]
			elif child.visits == most_visits:
				best_children.append(child)

		return choice(best_children)

	def simulate(self, expansion_count = 1):
		for i in range(expansion_count):
			current_node = self.root_node

			while current_node.expanded:
				current_node = current_node.get_preferred_child(self.root_node)

			self.expand(current_node)

	def expand(self, node):
		self.child_finder(node, self)

		for child in node.children:
			child_win_value = self.node_evaluator(child, self)

			if child_win_value != None:
				child.update_win_value(child_win_value)

			if not child.is_scorable():
				self.random_rollout(child)
				child.children = []

		if len(node.children):
			node.expanded = True

	def random_rollout(self, node):
		self.child_finder(node, self)
		child = choice(node.children)
		node.children = []
		node.add_child(child)
		child_win_value = self.node_evaluator(child, self)

		if child_win_value != None:
			node.update_win_value(child_win_value)
		else:
			self.random_rollout(child)