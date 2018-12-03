from multiprocessing import Process, Queue
from sympy import invert
class LCG:
	a = 25214903917
	c = 11
	m = 2**48-1
	state = 0

	def __init__(self, seed):
		self.state = self.init_scamble(seed)

	def init_scamble(self, seed):
		return (seed ^ 25214903917) & 281474976710655

	def next(self, bits):
		self.state = (self.a * self.state + self.c ) & self.m
		return (self.state >> 48 - bits) & ((1<<31) - 1)

	def nextInt(self, bound):
		return self.next(31) % bound


l = LCG(313373133731337)
# from java output

chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

# QC3qp3UgMUoWjSKgOtutFUglOu7W2rPRPGIu1g3RW6bpwTzWL9wvXALdyTYxa7GCWKFsRr1aRrzAFX0fz8gHkIFcYXpo7jSoVZat

key = "QC3qp3UgMUoWjSKgOt"
output = [chars.index(c) for c in key]
# output.reverse()
output.reverse()
# output2 = [l.nextInt(34) for _ in range(100)]
# output2.reverse()
# output = [16,33,6,20,5,29,10,2,2,27,8,16,21,26,10,1,1,14,31,6,10,23,13,4,2,18,6,14,22,5,7,23,13,5,7,7,18,17,16,2,9,26,11,33,20,0,17,31,0,14,25,13,31,22,8,31,32,11,31,8,2,17,31,33,8,25,3,2,31,29,12,28,21,1,29,26,27,32,12,3,6,26,27,11,30,7,21,30,32,31,4,10,3,21,0,7,17,2,21,13] # [l.nextInt(34) for _ in range(100)]
# print(output)
#output = output[:20]
# print(output2)

def find_low_seed(outputs):
	# These are the low bits of "bits"
	# So these are the 18th bits of the state
	low_bits = [i % 2 for i in outputs]
	candidates = []

	for i in range(2**18):
		# state = (i ^ 25214903917) & 281474976710655
		state = i
		succ = True
		for bit in low_bits:
			state = (25214903917 * state + 11) & 281474976710655
			if (state >> 17) % 2 != bit:
				succ = False
				break
		if succ:
			candidates.append(i)
	return candidates  # return all possible 17 bit values of lowest 17 bits of seed


def find_high_seed(candidates, output, bound, fr, to, q):
	"""
	Recover the 31 high bits of the seed via brute force
	"""
	poss_seeds = []
	mask = ((1<<31) - 1)
	for c in candidates:
		for i in range(fr, to):
			if not i % 100000000:
				print("At iter ", i)
			state = init_state = (i << 17) + c
			# state = (state ^ 25214903917) & 281474976710655
			succ = True
			for o in output:
				state = (25214903917 * state + 11) & 281474976710655
				out = (state >> 17) & mask
				if out % bound != o:
					succ = False
					break
			if succ:
				print("Found", init_state)
				poss_seeds.append(init_state)
	q.put(poss_seeds)
	print("DONE")


low_cands = find_low_seed(output)
print("Candidates for lowest 18 bits: ", low_cands)
state_cands = [] 

jobs = []
q = Queue()
for i in range(4):
	p = Process(target=find_high_seed, args=(low_cands, output, 62, i*1073741824, (i+1)*1073741824, q))
	p.start()
	jobs.append(p)

for j in range(len(jobs)):
	state_cands.extend(q.get())

for j in jobs:
	j.join()

def get_pref_state(state):
	a_m = invert(25214903917, 2**48)
	return (int(a_m) * (int(state) - 11)) & 281474976710655

def get_init_state_by_state(state):
	for i in range(80):
		state = get_pref_state(state)
	return state

print("Printing possible keys:")
for state in state_cands:
	l = LCG(0)
	l.state = get_init_state_by_state(state) # state
	outs = []
	for _ in range(100):
		outs.append(chars[l.nextInt(62)])
	outs.reverse()
	print("".join(outs))