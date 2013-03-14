#! /usr/bin/python3
from optparse import OptionParser
import csv
from math import *
from pylab import *

parser = OptionParser()
parser.add_option("-p","--plot", action="store_true",dest="plot_flag",default="False")
parser.add_option("-i","--input",action="store",type="string",dest="input_file",default="rawdata.csv")
parser.add_option("-o","--output",action="store",type="string",dest="output_file",default="output.csv")
parser.add_option("-w","--write",action="store_false",dest="write",default="True")
parser.add_option("-t","--tics",action="store",type="int",dest="tics",default=10)
parser.add_option("-l","--low",action="store",type="float",dest="min",default=0.0)
parser.add_option("-s","--summary",action="store_true",dest="summary",default="False")
parser.add_option("-u","--sort",action="store_true",dest="sort",default="False")
parser.add_option("-v","--trueplot",action="store_true",dest="trueplot",default="False")
(options, args) = parser.parse_args()

class approch:
	def __init__(self,name):
		self.name = name
		self.data = iterate(self.name)
		self.success = success(self.data)
		self.persentage = (self.success / float(len(self.data)))
		self.avrage = avrage(self.data)
		self.var = var(self)
		self.sd = sqrt(self.var)
		self.max = max(self.data)
		
	def summary(self):
		print"------------",self.name,"------------"
		print"Success rate: ",self.persentage
		print"Avrage value: ",self.avrage
		print"Maximum value:",self.max
		print"Variance:     ",self.var
		print"St. deviation:",self.sd
	
class struct:
	def __init__(self,name = options.input_file):
		self.t = colIndex("time")
		self.m = colIndex("method")
		self.d = colIndex("difficulty")
		self.c = colIndex("category")
		self.f = csv.reader(open(name,"r"),delimiter=',')
		
class output:
	def __init__(self,data = options.output_file):
		self.f = csv.write(open(name,"r"),delimiter=',')		

def colIndex(method):
	data = csv.reader(open(options.input_file,"r"),delimiter=',')
	return next(data).index(method)
	
def iterate(name):
	y = []
	x = struct()
	for n in x.f:
		if n[x.m] == name:
			y.append(float(n[x.t]))
	return sorted(y)

def success(data):
	x = 0
	for n in data:
		if n > options.min:
			x += 1
	return x
	
def avrage(data):
	x = []
	for n in data:
		if n > options.min:
			x.append(n)
	return sum(x) / len(x)

def var(data):
	x = []
	for n in data.data:
		if n > options.min:
			x.append(n**2-data.avrage**2)
	return sum(x) / (len(x) -1)
	
def plotND(data):
	x = np.linspace(options.min,data.max,500)
	plot(x,mlab.normpdf(x,data.avrage,data.sd))
	
def showPlot():
	grid(True)
	show()

def sdFunc(x,data):
	return e**(-(x-data.avrage)**2 / 2 / data.sd**2) / data.sd / sqrt(2 * pi)
	
		
draw = approch("draw")
mime = approch("mime")

if options.summary == True:
	draw.summary()
	mime.summary()
	
if options.plot_flag == True:
	plotND(draw)
	plotND(mime)
	showPlot()

