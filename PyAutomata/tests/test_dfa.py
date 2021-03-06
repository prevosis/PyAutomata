from unittest import TestCase
import PyAutomata as pa

class TestDFA(TestCase):
	"""
	Tests for adding states to DFA
	"""
	def test_add_state(self):
		d = pa.DFA()
		self.assertEqual(len(d.states), 1)
		state = 'state'
		d.add_state(state)
		self.assertEqual(len(d.states), 2)
		
	def test_add_multiple_states(self):
		d = pa.DFA()
		state1 = 'state1'
		state2 = 'state2'
		state3 = 'state3'
		d.add_states(state1, state2, state3)
		self.assertEqual(len(d.states), 4)

	def test_add_duplicate_states(self):
		d = pa.DFA()
		state1 = 'state1'
		state_1 = 'state1'
		d.add_states(state1, state_1)
		self.assertEqual(len(d.states), 2)

	"""
	Tests for adding transitions to DFA
	"""
	def test_add_transition(self):
		d = pa.DFA()
		d.add_symbol('a')
		d.add_state('next')
		d.add_transition(d.start, 'a', 'next')
		self.assertEqual(d.transition[d.start]['a'], 'next')

	def test_add_self_transition(self):
		d = pa.DFA()
		d.add_symbol('a')
		d.add_self_transition(d.start, 'a')
		self.assertEqual(d.transition[d.start]['a'], d.start)

	def test_add_many_self_transitions(self):
		d = pa.DFA()
		d.add_alphabet('a', 'b', 'c', 'd', 'e', 'f', 'g')
		d.self_transition_all(d.start)
		for i in range(len(d.sigma)):
			self.assertEqual(d.transition[d.start][d.sigma[i]], d.start)

	"""
	Tests for adding symbols to DFA
	"""
	def test_add_symbol(self):
		d = pa.DFA()
		d.add_symbol('a')
		self.assertEqual(len(d.sigma), 1)

	def test_add_many_symbols(self):
		d = pa.DFA()
		d.add_alphabet(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
		self.assertEqual(len(d.sigma), 12)

	def test_add_duplicate_symbol(self):
		d = pa.DFA()
		d.add_alphabet(1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
		self.assertEqual(len(d.sigma), 1)

	"""
	Tests for adding accepting/rejecting states to DFA
	"""
	def test_add_accepting_state(self):
		d = pa.DFA()
		d.add_accepting_state('accept')
		self.assertEqual('accept' in d.accepting, True)
		self.assertEqual(len(d.states), 2)

	def test_add_rejecting_state(self):
		d = pa.DFA()
		d.add_reject_state('reject')
		self.assertEqual(d.reject, 'reject')
		self.assertEqual(len(d.states), 2)

	"""
	Integration tests
	"""
	def test_replace_state(self):
		d = pa.DFA()
		d.add_states('q1', 'q2', 'q3')
		d.add_alphabet(1, 0)
		d.add_transition(d.start, 1, 'q1')
		d.add_self_transition(d.start, 0)
		d.add_transition('q1', 1, 'q2')
		d.add_transition('q1', 0, 'q3')
		d.add_transition('q2', 1, 'q3')
		d.add_transition('q2', 0, 'q1')
		d.self_transition_all('q3')
		self.assertEqual(len(d.states), 4)
		self.assertEqual(len(d.transition), 4)
		for key in d.transition:
			self.assertEqual(len(d.transition[key]), 2)
		old_transition = d.transition['q0']
		d.replace_state('q0', 'bs')
		self.assertEqual(len(d.states), 4)
		self.assertEqual(len(d.transition), 4)
		for key in d.transition:
			self.assertEqual(len(d.transition[key]), 2)
		self.assertEqual(old_transition, d.transition['bs'])

	def adding_state_after_adding_transitions(self):
		d = pa.DFA()
		d.add_states('q1', 'q2', 'q3')
		d.add_alphabet(1, 0)
		d.add_transition(d.start, 1, 'q1')
		d.add_self_transition(d.start, 0)
		d.add_transition('q1', 1, 'q2')
		d.add_transition('q1', 0, 'q3')
		d.add_transition('q2', 1, 'q3')
		d.add_transition('q2', 0, 'q1')
		d.self_transition_all('q3')
		self.assertEqual(len(d.states), 4)
		self.assertEqual(len(d.transition), 4)
		for key in d.transition:
			self.assertEqual(len(d.transition[key]), 2)
		d.add_state('newstate')
		for i in len(d.sigma):
			self.assertEqual(d.sigma[i] in d.transition['newstate'], True)

	"""
	Conserving determinism tests
	"""
	def test_no_more_than_one_transition_with_same_symbol(self):
		d = pa.DFA()
		d.add_states('q1', 'q2')
		d.add_alphabet(1, 0)
		d.add_transition('q1', 1, 'q2')
		d.add_self_transition('q1', 0)
		d.add_transition('q2', 0, 'q1')
		d.add_self_transition('q2', 1)
		d.add_state('q3')
		old_transition = d.transition['q2']
		d.add_transition('q2', 1, 'q3')
		self.assertEqual(d.transition['q2'], old_transition)

	"""
	Testing if strings are accepted by DFA
	"""
	def test_string_in_DFA(self):
		d = pa.DFA()
		d.add_alphabet(1, 0)
		d.add_states('A', 'BEF', 'CF', 'DF', 'F', 'B', 'C', 'D')
		d.add_accepting_state('A')
		d.add_accepting_state('BEF')
		d.add_accepting_state('DF')
		d.add_accepting_state('F')
		d.add_accepting_state('D')
		d.add_accepting_state('CF')
		d.start_state('A')
		d.add_reject_state('ø')
		d.add_transition('A', 0, 'ø')
		d.add_transition('A', 1, 'BEF')
		d.add_transition('BEF', 1, 'ø')
		d.add_transition('BEF', 0, 'CF')
		d.add_transition('CF', 1, 'ø')
		d.add_transition('CF', 0, 'DF')
		d.add_transition('DF', 0, 'F')
		d.add_transition('DF', 1, 'B')
		d.add_transition('F', 1, 'ø')
		d.add_self_transition('F', 0)
		d.add_transition('B', 1, 'ø')
		d.add_transition('B', 0, 'C')
		d.add_transition('C', 1, 'ø')
		d.add_transition('C', 0, 'D')
		d.add_transition('D', 0, 'ø')
		d.add_transition('D', 1, 'B') # should construct a DFA which accepts (100)* + 10*
		test_strings = [
			'100' * 100,
			'1' + '0' * 100,
			'1',
			'',
		]
		for string in test_strings:
			print(string)
			self.assertEqual(d.parse(string), True)
