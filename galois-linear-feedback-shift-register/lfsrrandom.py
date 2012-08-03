# Galois linear feedback shift register (LFSR) in Python
# Copyright (c) 2012 Nayuki Minase

import random


# Random number generator class (implements most functionality of random.Random)

class LfsrRandom(random.Random):
	
	def __new__(cls, *args, **kwargs):  # Magic because the superclass doesn't cooperate
		return random.Random.__new__(cls, random.random())
	
	
	def __init__(self, charis, state):
		assert isinstance(charis, int)
		assert isinstance(state, int)
		
		if charis < 0:
			raise ValueError("Invalid characteristic polynomial - negative")
		if charis.bit_length() < 2:
			raise ValueError("Invalid characteristic polynomial - degree too low")
		if state == 0:
			raise ValueError("Invalid state polynomial - all zero")
		if state.bit_length() >= charis.bit_length():
			raise ValueError("Invalid state polynomial - degree >= char poly degree")
		
		self.characteristic = charis
		self.degree = charis.bit_length() - 1
		self.state = state
	
	
	def randbit(self):
		result = self.state & 1                            # Use bit 0 in the LFSR state as the result
		self.state = self.state << 1                       # Multiply by x
		if (self.state >> self.degree) & 1 != 0:           # If degree of state polynomial matches degree of characteristic polynomial
			self.state = self.state ^ self.characteristic  # Then subtract the characteristic polynomial from the state polynomial
		return result
	
	
	def getrandbits(self, k):
		result = 0
		for i in xrange(k):
			result = (result << 1) | self.randbit()
		return result
	
	
	def random(self):
		return self.getrandbits(52) / float(1 << 52)



# Demo main program

if __name__ == "__main__":
	# Polynomial: x^16 + x^14 + x^13 + x^11 + x^0
	rand = LfsrRandom(0b10110100000000001, 1)
	for i in xrange(10):
		print rand.random()
	for i in xrange(20):
		print rand.randbit()