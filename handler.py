import random
import csv
import numpy as np

categories = ["kultur","vitenskap","natur","musikk","verden"]
cards = 296
cards = int(cards/5)
cards = np.linspace(1,cards,cards)

minTime = 5.0
maxTime = 60.0
tics = minTime
boundaries = []
mimeData = []
BmimeData = []
bnumbers = []

def randomNumber(mean,deviation):
	choice = random.randint(1,3)
	if  choice != 3:
		randData = random.normalvariate(mean,deviation)
	elif choice == 3:
		randData = random.uniform(minTime,maxTime+20)
	else:
		randData = 0
		
	if randData < minTime or randData > maxTime: 
		randData = 0
	return randData
	
def getMime():
	mean = 15.0
	deviation = 8.0
	data = randomNumber(mean,deviation)
	zeroBiaz = random.randint(1,3)
	if zeroBiaz == 3:
		data = 0
	return data
	
def getDraw():
	mean = 30.0
	deviation = 15.0
	data = randomNumber(mean,deviation)
	return data

def makeBound():
	n = 0
	while n < maxTime:
		n += tics
		boundaries.append(n)

def getBound(mimeData):
	for bound in boundaries:
		if mimeData <= bound and mimeData > bound - tics:
			mimeData = int(bound)
			return bound		
	return int(0)

def getDifficulty(s):
	chance = random.randint(1,6)
	if s == 0:
		if chance <= 3 and chance >= 1:
			return 3
		elif chance == 4 or chance == 5:
			return 2
		else:
			return 1
	else:
		if chance >= 1 and chance <= 3:
			return 1
		elif chance == 4 or chance == 5:
			return 2
		else:
			return 3		
			
def getRandomData()	:
	raw_file = open("raw_data.csv","wb")
	raw = csv.writer(raw_file)
	raw.writerow(["Time","Bound Time", "Type", "Category", "Difficulty"])
	
	for card in cards:
		for category in categories:
			if card % 2 != 0:
				Type = "mime"
				t = getMime()
			else:
				Type = "draw"
				t = getDraw()
	
			s = int(getBound(t))
			diff = getDifficulty(s)
			raw.writerow([t,s,Type,category,diff])
	raw_file.close()

makeBound()
getRandomData()

raw_file = open("raw_data.csv","r")
raw = csv.reader(raw_file)


mimeValue = []
drawValue = []
dataType = []

for row in raw:
	try:
		value = int(row[1])
		if str(row[2]) == "mime":
			mimeValue.append(value)
		elif str(row[2]) == "draw":
			drawValue.append(value)
		
	except:
		print "Error: not integer; "+str(row[1])
		
raw_file.close()
data_file = open("data.csv","wb")
data = csv.writer(data_file)

data.writerow(["mime","data"])
for bound in boundaries:
	count = mimeValue.count(bound)
	data.writerow([bound,count])
	
data.writerow(["draw","data"])
for bound in boundaries:
	count = drawValue.count(bound)
	data.writerow([bound,count])
	
data.writerow(["both","data"])
for bound in boundaries:
	count = mimeValue.count(bound)+drawValue.count(bound)
	data.writerow([bound,count])
	
	

	
	


















