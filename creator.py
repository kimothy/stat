""" Random data generator """
import random as rdm
import csv
from optparse import OptionParser


""" Default Values """
Cards = 296					# number of question cards in deck
Min = 5.0					# minimum answer time
Max = 60.0					# maximum answer time
Msd = 7.0					# mime standard deviation
Mav = 15.0					# mime avrage answer time
Dsd = 15.0					# draw standard deviation
Dav = 30.0					# draw avrage answer time
Bias = 0.3					# bias. mime vs. draw
Mean = Max / 2				# default mean value
Deviation = Max / 4			# default deviation value
data_file = "rawdata.csv"	# default name for data file
Categories = ["kultur","vitenskap","natur","musikk","verden"]
Methods = ["mime","draw"]


""" Option Parser """
parser = OptionParser()
parser.add_option("-c", dest="cards",help="number of cards in deck")

parser.add_option("-i","--min", dest="min",help="minimum answer time")

parser.add_option("-a","--max", dest="max",help="maximum answer time")

parser.add_option("-s","--msd", dest="msd",help="standard deviation for mime data")

parser.add_option("-v","--mav", dest="mav",help="mean of mime data")

parser.add_option("-t","--dsd", dest="dsd", help="standard deviation for draw data")

parser.add_option("-w","--dav", dest="dav",help="mean of draw data")

parser.add_option("-b","--bias", dest="bias",help="mime vs. draw bias")
 
parser.add_option("-f","--file", dest="data_file",help="set filename",metavar="file")
 
(options, args) = parser.parse_args()


""" Option handler """
if options.cards != None:
	Cards = options.cards

if options.min != None:
	Min = options.min
	
if options.max != None:
	Max = options.max
	
if options.msd != None:
	Msd = options.msd
	
if options.mav != None:
	Mav != options.mav
	
if options.dsd != None:
	Dsd = options.dsd
	
if options.dav != None:
	Dav = options.dav
	
if options.bias != None:
	Bias != options.bias
	
if options.data_file != None:
	data_file = data_file

print "Cards =", Cards,"Min =", Min,"Max =",Max,"Bias =", Bias
print "Msd =", Msd,"Mav =",Mav,"Dsd =", Dsd,"Dav =",Dav


""" Fuctions """
def time(method, Bias):
	if method == Methods[0]:
		Mean = Mav
		Deviation = Msd
		Biaz = Bias * 0.5
	elif method == Methods[1]:
		Mean = Dav
		Deviation = Dsd
		Biaz = (1 - Bias) * 0.5
	else:
		print "Time() error: Cant recognize method; ",method
		Mean = Max / 2
		Deviation = Max / 4
		Bias = 0.25
	
	chance = rdm.random()	
	if chance > Biaz:
		if chance <= 0.5 and chance >= 0:
			return rdm.normalvariate(Mean,Deviation)
		elif chance > 0.5 and chance <= 1:
			return rdm.uniform(Min,Max+20)
		else:
			print "Time() error: chance error; ",chance
			return Max / 2
	elif chance < Biaz:
		return 0
	else:
		print "Time() error: Biaz error; ",Biaz
		return 0
	
def difficulty(t):
	chance = rdm.random()
	if chance <= 0.5 and t != 0 or chance >= 0.8 and t == 0:
		return 1
	elif chance > 0.5 and chance < 0.8:
		return 2
	elif chance >= 0.8 and t != 0 or chance <= 0.5 and t == 0:
		return 3
	else:
		print "difficulty() error: chance error; ",chance
		return 2
	

""" Main Program """
data_file = open(data_file,"wb")
data = csv.writer(data_file)
data.writerow(["Method","Category","Difficulty","Time"])

n = 0
while n < Cards:
	for category in Categories:
		for method in Methods:
			n += 1
			if n < Cards:
				t = time(method, Bias)
				if t < 0 or t > Max:
					t = 0
				d = difficulty(t)
				data.writerow([method,category,d,t])
