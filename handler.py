""" Data handler """
import csv
from optparse import OptionParser


""" Default Values """
tics = 10.0
method = ["mime","draw"]
file_name = "rawdata.csv"	# default name for data file
Max = 0
Check = False

""" Option Parser """
parser = OptionParser()
 
parser.add_option("-f","--input", dest="file_name",help="data filename",metavar="file")

parser.add_option("-s","--output", dest="save_file",help="save filename",metavar="file")

parser.add_option("-t","--task",dest="task", help = "Task: Valid options; 'method'", metavar="task")

parser.add_option("-i","--tics",dest="tics", help = "Sets data tics", metavar="tics")

(options, args) = parser.parse_args()

""" Options Handler """
if options.file_name != None:
	file_name = options.data_file
if options.task != None:
	task = options.task
if options.tics != None:
	tics = int(options.tics)
if options.save_file != None:
	save_file = str(options.save_file)
else:
	save_file = str(options.task)+"_output.cvs"
	
print "Opening",file_name
print "Saving to", save_file

""" Functions """
def maxValue():
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

def getBounderies():
	bounderies = []
	n = 0
	while n < Max:
		n += tics
		bounderies.append(int(n))
	return bounderies
	
def methodStats(method):
	n = 0
	
	save.writerow(["methodStats",method])
	for tic in bounderies:
		for row in data:
			if row[0] == method or row[0] == "both" and row[3] > tic-tics and row [3] < tic:
				n += 1
				
		save.writerow([tic,n])
				

""" Main Program """
data_file = open(file_name,"r")
data = csv.reader(data_file)

savefile = open(save_file,"wb")
save = csv.writer(savefile)
	
if options.task == "method":
	Max = maxValue()
	bounderies = getBounderies()
	methodStats("both")
	methodStats("mime")
	methodStats("draw")
	




				
			



















