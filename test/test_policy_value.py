import unittest
from montecarlo.node import Node
from montecarlo.montecarlo import MonteCarlo

class TestPolicyValue(unittest.TestCase):

	def test_choice_is_correct(self):
		montecarlo = MonteCarlo(Node(0))
		montecarlo.child_finder = self.child_finder

		montecarlo.simulate(50)

		chosen_node = montecarlo.make_choice()
		self.assertIs(chosen_node.state, 1)

	def child_finder(self, node, montecarlo):
		node.add_children(self.build_children(node))
		node.update_win_value(node.state)

	def build_children(self, node):
		children = []

		for i in range(2):
			child = Node(node.state or (1 if i == 1 else -1))
			child.policy_value = .90 if i == 1 else 0.10
			children.append(child)

		node.update_win_value(0)

		return children