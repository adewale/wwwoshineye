"""
WikiNeighbour.py
Usage: wikiNeighbour.py with links.txt in the same directory.

This processes a link database in the format described at 
http://c2.com/cgi/wiki?WikiMines and lists the people who are closest to each
other. Proximity is worked out by assigning a point for each wiki page that 
both person and otherPerson are present on.
With a sufficiently useful links.txt file this can tell you which people
in a wiki you should be paying attention to based on past behaviour.
The only link database that this script is known to work with is available from
http://c2.com/wiki/links.zip

Trivia:
The original idea came Bryce at XTC just before christmas 2002.
I'd be interested if anyone implements the same idea for mailing lists or newsgroups.
"""
#wiki neighbour identification scripts
#globals
cache = {}

#modify this to show more or less neighbours
NEIGHBOURS_TO_SHOW = 5

def processLinks():
	"""Process links file. 
	Doesn't currently deal with | properly but it doesn't seem to be a problem."""
	file = open("links.txt")
	pages = {}#pages = {pageName -> linkList}
	for line in file:
		links = line.split()
		key = links[0]#extract page name
		pages[key] = links[1:]#store page's contents except title
	return pages

def findPeople(pages):
	"find people in the pages by looking for CategoryHomePage"
	people = []
	for pageName in pages:
		links = pages[pageName]
		lastLink = links[-1:]#slicing using -1 gets the last element safely even when the list is empty
		if (len(lastLink)>0) and lastLink[-1] == "CategoryHomePage":
			people.append(pageName)
	return people

def generateRatings(pages, people):
	#for each person rate all other persons
	#ratings = {person -> {score ->[otherPerson]}}
	from time import time
	globalRatings = {}
	for person in people:
		globalRatings[person] = calculatePersonalRating(pages, people, person)
	return globalRatings

def calculatePersonalRating(pages, people, person):
	personalRatings = {}
	for otherPerson in people:
		if person is otherPerson:
			continue#dont' rate yourself
		
		proximityNumber = cachedCalculateProximity(person, otherPerson, pages)
					
		#a proximityNumber means that person is infinitely far away and can be ignored
		if proximityNumber == 0:
			continue
		
		if not personalRatings.has_key(proximityNumber):
			personalRatings[proximityNumber] = []
		
		personalRatings[proximityNumber].append(otherPerson)
	return personalRatings

def cachedCalculateProximity(person, otherPerson, pages):
	#create canonical string to act as a key
	l = [person, otherPerson]
	l.sort()
	key = l[0] + l[1]
	if not cache.has_key(key):
		cache[key] = calculateProximity(person, otherPerson, pages)
	return cache[key]

def calculateProximity(person, otherPerson, pages):
	"""Calculate the proximity for these two people.
	Proximity is the number of pages on which they both appear."""
	score = 0
	for pageName in pages:
		linkList = pages[pageName]
		if person in linkList and otherPerson in linkList:
			score += 1
	return score

def printRatings(globalRatings):
	#sort people in alphabetical order
	keys = globalRatings.keys()
	keys.sort()

	for person in keys:
		personalRatings = globalRatings[person]
		print person
		print "=" * len(person)
		
		scores = personalRatings.keys()
		scores.sort(lambda before, after: after-before)#sort scores in descending order
		for score in scores[:NEIGHBOURS_TO_SHOW]:#only show the top n neighbours
			print score, "::", ", ".join(personalRatings[score])
		print


def main():
	from time import time
	t1 = time()
	pages = processLinks()
	print "processLinks() took:: ", time()-t1
	
	t1 = time()
	people = findPeople(pages)
	print "findPeople(pages) took:: ", time()-t1
	
	t1 = time()
	globalRatings =  generateRatings(pages, people)
	print "generateRatings(pages, people) took:: ", time()-t1

	printRatings(globalRatings)

if __name__=='__main__':
	main()