import sys
import random

class PrimeGenerator(object):

	def __init__(self, **kwargs):
		bits = debug = None
		if 'bits' in kwargs:
			bits = kwargs.pop('bits')
		if 'debug' in kwargs:
			debug = kwargs.pop('debug')

		self.bits = bits
		self.debug = debug
		self._largest = (1 << bits) -1

	def set_initial_candidate(self):
		candidate = random.getrandbits(self.bits)
		if candidate & 1 == 0:
			candidate += 1
		candidate |= (1 << self.bits-1)
		candidate |= (2 << self.bits-3)
		self.candidate = candidate

	def set_probes(self):
		self.probes = [2, 3, 5, 7, 11, 13, 17]

	def test_candidate_for_prime(self):
		p = self.candidate
		if p == 1:
			return 0
		if p in self.probes:
			self.probability_of_prime = 1
			return 1
		if any([p%a == 0 for a in self.probes]):
			return 0

		k, q = 0, self.candidate - 1
		while not q&1:
			q >>= 1
			k += 1
		if self.debug:
			print('q = ' + q + ' k = ' + k)

		for a in self.probes:
			a_raised_to_q = pow(a, q, p)
			if a_raised_to_q == 1 or a_raised_to_q == p-1:
				continue
			a_raised_to_jq = a_raised_to_q
			primeflag = 0
			for j in range(k-1):
				a_raised_to_jq = pow(a_raised_to_jq, 2, p)
				if a_raised_to_jq == p-1:
					primeflag = 1
					break
			if not primeflag:
				return 0
		self.probability_of_prime = 1 - 1.0/(4 ** len(self.probes))
		return self.probability_of_prime

	def findPrime(self):
		self.set_initial_candidate()
		if self.debug:
			print(" candidate is " + self.candidate)
		self.set_probes()
		if self.debug:
			print(" The probes are " + str(self.probes))

		max_reached = 0
		while 1:
			if self.test_candidate_for_prime():
				if self.debug:
					print("Prime Number: %d with probability %f\n" %(self.candidate, self.probability_of_prime))
				break
			else:
				if max_reached:
					self.candidate -= 2
				elif self.candidate >= self._largest - 2:
					max_reached = 1
					self.candidate -= 2
				else:
					self.candidate += 2
				if self.debug:
					print(" candidate is: %d" %self.candidate)
		return self.candidate

