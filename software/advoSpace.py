usage = """
python advoSpace.py -c[ertfile] FILENAME -r[atingfile] FILENAME

The certfile should be a copy of http://www.advogato.org/person/
The ratingfile should be a copy of http://www.advogato.org/rating/report/USERNAME for the user whose perspective on
the advogato reputation space you wish to see.

v1.1
"""
import sys, getopt, re

def main():
	options, args = getopt.getopt(sys.argv[1:], "c:r:", ["certfile", "ratingfile="])
	
	if (len(options) < 2):
		print usage
		sys.exit()
	
	certsFileName = options[0][1]
	ratingsFileName = options[1][1]

	certMap = makeCertMap(certsFileName)
	addDiaryRatings(certMap, ratingsFileName)

	personList = makePersonList(certMap)
	advoSpace = Grid(personList)
	
	
	page = """
	<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
	<html>
	<head><title>Advospace</title></head>
	<body bgcolor="#ffffff">
	
	""" + advoSpace.getHtmlTable() + """
	
	</body>
	</html>
	"""
	
	file = open("advoSpaceOutput.html", "w")
	file.write(page)
	file.close()

def makeCertMap(certsFileName):
	"Create a dictionary of usernames mapped to certification levels using data from certsFileName"
	pattern = re.compile("""^<div class="(level\d)"><a href="(.*)/">.*</a>.*, (.*)$""")
	file = open(certsFileName)
	results = {}
	for line in file:
		match = pattern.search(line)
		if (match):
			groups = match.groups()
			results[groups[1]] = [groups[2]]
	return results

def addDiaryRatings(certMap, ratingsFileName):
	"Add ratings to certMap using data from ratingsFileName"
	pattern = re.compile("""^d/(.*): ([\d\.]+) &""")#d/axlnikon: 1 &plusmn;0.0 (confidence .0069)<br>, !alert
	file = open(ratingsFileName)
	for line in file:		
		match = pattern.search(line)
		if (match):
			groups = match.groups()
			name = groups[0]
			rating = groups[1]
			if (name not in certMap):#diary rating but no cert!
				continue
			certMap[name].append(rating)

def makePersonList(certMap):
	"Convert the certMap into a list of Person objects"
	personList = []
	for name in certMap:
		cert = certMap[name][0]
		if (len(certMap[name]) < 2):#user with cert but no diary rating
			rating = -1
		else:
			rating = certMap[name][1]
		personList.append(Person(name, cert, rating))
	return personList

class Person:
	"A representation of a person within the Advogato reputation space"
	def __init__(self, userName, cert, rating):
		self. userName = userName
		self.cert = cert
		self.rating = rating
	
	def __str__(self):
		return "::".join([self. userName, self. cert, str(self. rating)])

class Cell:
	"""
	Currently a point in Advogato's 2-dimensional reputation space but adding more dimensions
	would be relatively easy as long as you had a way to visualise the extra data. A Cell holds a list of persons
	"""
	def __init__(self):
		self.persons = []

	def add(self, person):
		self.persons.append(person)

class Grid:
	"A 2-dimensional array of Cell instances"
	NUMBER_OF_CERT_LEVELS = 4
	NUMBER_OF_RATINGS_TYPES = 102
	UNRATED = 101
	
	certValues = {"Observer": 0, "Apprentice": 1, "Journeyer": 2, "Master": 3}
	certStrings = {0:"Observer", 1: "Apprentice", 2: "Journeyer", 3: "Master"}
	def __init__(self, persons):
		#initialise list of lists containing Cell instances--this should be an array of some kind
		self.cells = []
		for row in xrange(Grid.NUMBER_OF_RATINGS_TYPES):#ratings including none(represented as -1) then 0.0 to 10.0
			temp = []
			for col in xrange(Grid.NUMBER_OF_CERT_LEVELS):#4 levels from observer to master
				temp.append(Cell())
			self.cells.append(temp)

		#populate the grid
		for person in persons:
			row = self.convertToRow(person.rating)
			col = self.convertToColumn(person.cert)
			self.cells[row][col].add(person)
	
	def getHtmlTable(self):
		table = """<table border="1">\n"""		
		table += "<tr><th></th>"
		for i in xrange(Grid.NUMBER_OF_CERT_LEVELS):
			table += "<th>" + Grid.certStrings[i] + "</th>\n"
		table +="</tr>\n"
		
		rowNumber = -1.0
		for row in self.cells:
			rowNumber += 1.0
			#ignore unrated diaries
			if rowNumber == Grid.UNRATED:
				break
			
			#ratings below 1.0 don't happen so that row is empty and can be ignored
			if rowNumber < 10:
				continue
			
			table += "<tr>\n" + "<td>" + self.convertToRating(rowNumber) + "</td>"
			for col in row:
				table += "<td>"
				for person in col.persons:
					table += str(person) + "<br>\n"
				table += "</td>\n"
			table += "</tr>\n"

		table += "</table>\n"
		return table

	def convertToRating(self, rowNumber):
		if rowNumber == Grid.UNRATED:
			return "No rating"
		else:
			return str(rowNumber / 10)

	def convertToRow(self, rating):
		"Convert rating from -1, 1.0-10 to 0-101 inclusive with 101 being used for -1"
		rating = float(rating)
		if rating == -1:
			return Grid.UNRATED
		else:
			return int(rating * 10)
	
	def convertToColumn(self, cert):
			return Grid.certValues[cert]

if __name__=='__main__':
	main()	
