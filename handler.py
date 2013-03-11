#! /usr/bin/python3
from optparse import OptionParser
import csv
from math import *

parser = OptionParser()
parser.add_option("-p","--plot", action="store_true",dest="plot_flag",default="False")
parser.add_option("-i","--input",action="store",type="string",dest="input_file",default="rawdata.csv")
parser.add_option("-o","--output",action="store",type="string",dest="output_file",default="output.csv")
parser.add_option("-w","--write",action="store_false",dest="write",default="True")
parser.add_option("-t","--tics",action="store",type="int",dest="tics",default=10)
parser.add_option("-m","--method",action="store_true",dest="method",default="False")
(options, args) = parser.parse_args()
print("Opening",options.input_file,"and saving to",options.output_file)

def openInput(column = "time"):
	data = csv.reader(open(options.input_file,"r"),delimiter=',')
	col = next(data).index(column)
	return {'data':data,'col':col}

def colSum(method,col = "time"):
	inFile = openInput()
	return sum(float(row[inFile['col']]) for row in inFile['data'])
	
def colRows():
	x = 0
	for row in openInput()['data']:
		x += 1
	return x
						
def limits():
	lim = {}
	lim['0'] = 0
	for x in range(options.tics,int(largest("time"))+options.tics,options.tics):
		lim[str(x)] = 0
	return lim
	
def avrage(method):
	return colSum(method) / colRows(method)
	
def largest(col):
	inFile = openInput(col)
	return max(float(row[inFile['col']]) for row in inFile['data'])
	
def sortMethod():
	ix = {'t':openInput("time")['col'],'m':openInput("method")['col']}
	data = {'draw':limits(),'mime':limits()}
	for limit in limits():
		for row in openInput()['data']:
			if float(row[ix['t']]) >= float(limit)-options.tics and float(row[ix['t']]) < float(limit):
					temp = (data[str(row[ix['m']])])
					temp[str(limit)] += 1
					data[str(row[ix['m']])] = temp
	return data
			
def sd(method):
	inFile = openInput("time")
	avr = avrage(method)
	x = 0
	for row in inFile["data"]:
		x += (float(row[inFile['col']])-float(avr))**2
		
	x = sqrt(x / (colRows(method) -1))
	return x

if options.method == True:
	print("Avrage:",avrage())
	print("Standard deviation:",sd())

	
	
	
