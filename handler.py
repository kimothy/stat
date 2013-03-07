""" Data handler """
import csv
from optparse import OptionParser
import sys
from pylab import *
import matplotlib.pyplot as plt

""" Default Values """
tics = 10.0
method = ["mime","draw"]
file_name = "rawdata.csv"	# default name for data file
Max = 0
Bounderies = []
drawValues = []
mimeValues = []
bothValues = []

""" Option Parser """
parser = OptionParser()
 
parser.add_option("-r","--read", dest="file_name",help="data filename",metavar="file")

parser.add_option("-s","--save", dest="save_file",help="save filename",metavar="file")

parser.add_option("-i","--tics",dest="tics", help = "Sets data tics", metavar="tics")

parser.add_option("-t","--task",dest="task", help = "Task: Valid options; 'method'", metavar="task")

parser.add_option("-p","--plot",dest="plot", help = "Plot", metavar="True")

(options, args) = parser.parse_args()

""" Options Handler """
if options.file_name != None:
	file_name = options.data_file
if options.task != None:
	task = options.task
else:
	sys.exit("ERROR; no task selected")
	
if options.tics != None:
	tics = int(options.tics)
if options.save_file != None:
	save_file = str(options.save_file)
else:
	save_file = str(options.task)+"_output.cvs"
	
print "Opening %s, and saving to %s" %(file_name,save_file)

""" Functions """
def points():
	data_file = open(file_name,"r")
	data = csv.reader(data_file)
	points = -1
	data = csv.reader(data_file)
	for row in data:
		points += 1	
	return points
	
def bounderies():
	for x in xrange(int(tics),int(Max+tics),int(tics)):
		Bounderies.append(x)
	print "Bouderies:",Bounderies
	
def maxValue():
	data_file = open(file_name,"r")
	data = csv.reader(data_file)
	X = 0
	for row in data:
		try:
			if row[3] == "Time":
				Check = True
			elif float(row[3]) > float(X):
				X = float(row[3])
		except:
			print "ERROR: Faild to read file;", file_name
	print "Maximum value:",X
	return X

def methodArrays():
	save.writerow(["group","both","mime","draw"])
	dataArray = []
	for bound in Bounderies:
		data_file = open(file_name,"r")
		data = csv.reader(data_file)
		x = [0,0]
		for item in data:
			try:
				if float(item[3]) != 0 and float(item[3]) >= float(bound)-float(tics) and float(item[3]) < float(bound) and (item[0] == "mime"):
					x[0] += 1
				elif float(item[3]) != 0 and float(item[3]) >= float(bound)-float(tics) and float(item[3]) < float(bound) and (item[0] == "draw"):
					x[1] +=1
			except:
				if item[3] != "Time":
					print "methodArrays() ERROR: could not convert to float;",item[3]
		drawValues.append(x[0])
		mimeValues.append(x[1])
		bothValues.append(x[0]+x[1])
		save.writerow([int(bound),x[0]+x[1],x[0],x[1]])

""" Main Program """
data_file = open(file_name,"r")
data = csv.reader(data_file)

points = points()
print "Number of data points: %d" %(points)

savefile = open(save_file,"wb")
save = csv.writer(savefile)

if options.task == "method":
	Max = maxValue()
	bounderies()
	dataArray = methodArrays()
	if options.plot == "True":
		print "Combined",bothValues
		print "Mime Values",mimeValues
		print "Draw Values",drawValues
		plt.plot(Bounderies,bothValues,Bounderies,mimeValues,Bounderies,drawValues)
		plt.show()
		
			
				
				
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

