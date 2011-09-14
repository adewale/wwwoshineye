#!/usr/bin/python

"""
Take a function f and return a function f_memoised that is the same as f except it uses
cacheing.
Uses Python 2.2
"""
import time
	
def memoise(f):
	cache = {}
	def f_memoised(*args):
		if args not in cache:
			cache[args] = apply(f, args)
		return cache[args]
	return f_memoised

def test(function, arguments):
	TEST_ITERATIONS = 100000
	startTime = time.time()
	for x in xrange(TEST_ITERATIONS):
		result = apply(function, arguments)
	endTime = time.time()
	print "Result is ", result
	return endTime - startTime

if __name__=='__main__':
	def factorial(n):
		if n > 1:
			return n * factorial(n-1)
		else:
			return 1

	def intersperse(arg1, arg2):
		"intersperse arg2 with arg1 so that every other character of arg2 is arg1"
		return arg1.join(arg2)

	memoised_factorial = memoise(factorial)
	memoised_intersperse = memoise(intersperse)

	functions = [intersperse, memoised_intersperse, factorial, memoised_factorial]
	arguments = [("|", "HelloWorld"),("|", "HelloWorld"),(10,),(10,)]
	index = 0
	for f in functions:
		print "Testing %s took %.3f seconds" % (f.__name__, test(f, arguments[index]))
		index += 1
	