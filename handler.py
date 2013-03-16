#! /usr/bin/python3
from optparse import OptionParser
import csv
from math import *
from pylab import *
import numpy as np
from scipy.stats import norm
from matplotlib import rc

parser = OptionParser()
parser.add_option("-p","--plot", action="store_true",dest="plot_flag",default="False")
parser.add_option("-i","--input",action="store",type="string",dest="input_file",default="rawdata.csv")
parser.add_option("-o","--output",action="store",type="string",dest="output_file",default="output.csv")
parser.add_option("-w","--write",action="store_false",dest="write",default="True")
parser.add_option("-t","--tics",action="store",type="int",dest="tics",default=10)
parser.add_option("-l","--low",action="store",type="float",dest="min",default=0.0)
parser.add_option("-s","--summary",action="store_true",dest="summary",default="False")
parser.add_option("-u","--sort",action="store_true",dest="sort",default="False")
parser.add_option("-f","--tex",action="store_true",dest="tex",default="False")
parser.add_option("-c","--ci",action="store",type="float",dest="ci",default=0.90)

(options, args) = parser.parse_args()

class approch:
	def __init__(self,name,color = 'blue'):
		self.name = name
		self.data = iterate(self.name)
		self.success = success(self.name)
		self.persentage = (float(self.success[0]) / float(self.success[1]))
		self.average = np.average(self.data)
		self.median = np.median(self.data)
		self.var = np.var(self.data)
		self.sd = std(self.data)
		self.max = max(self.data)
		self.color = color
	def ciMin(self,persentage):
		return self.average - self.sd * norm.ppf((1-persentage)/2)
	def ciMax(self,persentage):
		return self.average + self.sd * norm.ppf((1-persentage)/2)
		
	def summary(self):
		print"------------",self.name,"------------"
		print"Success rate:  %d/%d, %.2f" % (self.success[0],self.success[1],self.persentage)
		print"Avrage value: ",self.average
		print"Median:       ",self.median
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

def largest():
	if draw.max > mime.max:
		return draw.max
	elif draw.max < mime.max:
		return mime.max

def colIndex(method):
	data = csv.reader(open(options.input_file,"r"),delimiter=',')
	return next(data).index(method)
	
def iterate(name):
	y = []
	x = struct()
	for n in x.f:
		if n[x.m] == name and float(n[x.t]) != -1:
			y.append(float(n[x.t]))
	return sorted(y)

def success(name):
	x = struct()
	y = [0,0]
	for n in x.f:
		if n[x.m] == name:
			y[1] += 1
			if float(n[x.t]) != -1:
				y[0] += 1
	return y
	
def plotND(data):
	x = np.linspace(options.min,largest(),500)
	plot(x,mlab.normpdf(x,data.average,data.sd),label = data.name,color = data.color)
	
def plotCI(data,persentage = options.ci):
	x = np.linspace(data.ciMin(persentage),data.ciMax(persentage),300)
	fill_between(x,mlab.normpdf(x,data.average,data.sd),0,alpha = 0.1,color = data.color)
	
def showPlot(tex = False):
	if tex == True:
		rc('text', usetex=True)
		rc('font', family='serif')
		xlabel(r'\textbf{tid}')
		ylabel(r'\texbf{sansynlighet}')
	else:
		xlabel('time')
		ylabel('probability')
		
	legend(loc = 'upper right')
	grid(True)
	show()

def sdFunc(x,data):
	return e**(-(x-data.avrage)**2 / 2 / data.sd**2) / data.sd / sqrt(2 * pi)
			
draw = approch("draw",'green')
mime = approch("mime",'blue')

if options.summary == True:
	draw.summary()
	mime.summary()
	
if options.plot_flag == True:
	plotND(draw)
	plotND(mime)
	plotCI(draw)
	plotCI(mime)
	showPlot(options.tex)
	
