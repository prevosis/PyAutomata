class DFA:
	def __init__(self):
		self.states = ['q0']
		self.sigma = []
		self.transition = {'q0': {}}
		self.start = 'q0'
		self.accepting = []
		self.reject = None

	def __str__(self):
		ret = 'Q: {' + ', '.join(self.states) + '}\n'
		ret += '∑: {' + ', '.join([str(self.sigma[i]) for i in range(len(self.sigma))]) + '}\n'
		ret += '∂: \n{\n'
		for i in range(len(self.states)):
			for j in range(len(self.sigma)):
				ret += '\t∂(' + self.states[i] + ', ' + str(self.sigma[j]) + ') = ' 
				ret += str(self.transition[self.states[i]][self.sigma[j]])
				ret += '\n'
		ret += '}\n'
		ret += 's: ' + self.start + '\n'
		ret += 'F: {' + ', '.join(self.accepting) + '}'
		return ret
 
	def add_state(self, state):
		if state not in self.states:
			self.states.append(state)
			self.transition[state] = {}
			for i in range(len(self.sigma)):
				self.transition[state][self.sigma[i]] = ''

	def add_states(self, *args):
		for state in args:
			self.add_state(state)

	def add_transition(self, state, symbol, output):
		symbol = str(symbol)
		if not self.transition[state][symbol]:
			self.transition[state][symbol] = output

	def add_self_transition(self, state, symbol):
		symbol = str(symbol)
		self.add_transition(state, symbol, state)

	def self_transition_all(self, state):
		for symbol in self.sigma:
			self.add_self_transition(state, symbol)

	def add_symbol(self, symbol):
		symbol = str(symbol)
		if symbol not in self.sigma:
			self.sigma.append(symbol)
			for i in range(len(self.states)):
				self.transition[self.states[i]][symbol] = ''

	def add_alphabet(self, *args):
		for symbol in args:
			self.add_symbol(symbol)

	def add_accepting_state(self, state):
		self.accepting.append(state)
		self.add_state(state)

	def add_reject_state(self, state='reject'):
		self.add_state(state)
		self.reject = state
		self.self_transition_all(state)

	def remove_state(self, state):
		self.states.remove(state)
		del self.transition[state]
		if state in self.accepting:
			self.accepting.remove(state)

	def replace_state(self, old, new):
		try:
			index = self.states.index(old)
		except ValueError:
			print('Invalid state')
		try:
			old_transition = self.transition[old]
		except KeyError:
			print('Invalid state')
			return
		for i in self.transition.keys():
			for j in self.sigma:
				if self.transition[i][j] == old:
					self.transition[i][j] = new
		self.remove_state(old)
		if new not in self.states:
			self.states.append(new)
		self.transition[new] = old_transition
		if self.start == old:
			self.start = new

	def start_state(self, state):
		self.replace_state(self.start, state)

	def parse(self, string=''):
		curr = self.start
		if not string:
			return self.start in self.accepting
		for i in range(len(string)):
			ch = string[i]
			if ch not in self.sigma:
				return False
			curr = self.transition[curr][ch]
		return curr in self.accepting