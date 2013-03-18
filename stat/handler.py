#! /usr/bin/env python
import pygtk
import gtk
import gobject

import time

import csv

import numpy as np
from scipy.stats import norm
from pylab import *

from matplotlib.figure import Figure
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar

from optparse import OptionParser
parser = OptionParser()
parser.add_option("-i","--input",action="store",type="string",dest="input_file",default="rawdata.csv")
(options, args) = parser.parse_args()

class Base:
	""" main GTK window and manipulating functions """
	def destroy(self,widget, data = None):
		print "terminated" 
		gtk.main_quit()
		
	def set_avgDraw(self,slider_info):
		""" Offset for average draw value"""
		self.avgDraw = slider_info.get_value()
		make_plot()
		
	def set_avgMime(self,slider_info):
		""" Offset for draw standard distribution"""
		self.avgMime = slider_info.get_value()
		make_plot()
		
	def set_sdDraw(self,slider_info):
		""" Offset for draw standard distribution"""
		self.sdDraw = slider_info.get_value()
		make_plot()
		
	def set_sdMime(self,slider_info):
		""" Offset for draw standard distribution"""
		self.sdMime = slider_info.get_value()
		make_plot()
		
	def reset_adjustments(self,x):
		self.avgDraw = 0
		self.avgMime = 0
		self.sdDraw = 0
		self.sdMime = 0
		self.mslider1.set_adjustment(gtk.Adjustment(value=0, lower=-20, upper=20, step_incr=1, page_incr=0, page_size=0))
		self.mslider2.set_adjustment(gtk.Adjustment(value=0, lower=-5, upper=5, step_incr=1, page_incr=0, page_size=0))
		self.mslider3.set_adjustment(gtk.Adjustment(value=0, lower=-20, upper=20, step_incr=1, page_incr=0, page_size=0))
		self.mslider4.set_adjustment(gtk.Adjustment(value=0, lower=-5, upper=5, step_incr=1, page_incr=0, page_size=0))
		make_plot()

		
	def __init__(self):
		self.avgDraw = 0
		self.avgMime = 0
		self.sdDraw = 0
		self.sdMime = 0
		
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.set_size_request(1000,600)
		self.window.set_title("MA-155 STAT")
			
		self.mslider1 = gtk.HScale(adjustment=gtk.Adjustment(value=0, lower=-20, upper=20, step_incr=0.1, page_incr=0, page_size=0))
		self.mslider1.connect("value_changed",self.set_avgDraw)
		self.mslider2 = gtk.HScale(adjustment=gtk.Adjustment(value=0, lower=-5, upper=5, step_incr=0.1, page_incr=0, page_size=0))
		self.mslider2.connect("value_changed",self.set_sdDraw)
		self.mslider3 = gtk.HScale(adjustment=gtk.Adjustment(value=0, lower=-20, upper=20, step_incr=0.1, page_incr=0, page_size=0))
		self.mslider3.connect("value_changed",self.set_avgMime)
		self.mslider4 = gtk.HScale(adjustment=gtk.Adjustment(value=0, lower=-5, upper=5, step_incr=0.1, page_incr=0, page_size=0))
		self.mslider4.connect("value_changed",self.set_sdMime)
		
		self.draw_tools = gtk.Table(rows = 4, columns = 2, homogeneous = False)
		self.draw_tools.attach(gtk.Label("Average"),0,2,0,1)
		self.draw_tools.attach(self.mslider1,0,2,1,2)
		
		self.draw_tools.attach(gtk.Label("Distribution"),0,2,2,3)
		self.draw_tools.attach(self.mslider2,0,2,3,4)
		
		self.draw_adj_frame = gtk.Frame(label = "Adjustments")
		self.draw_adj_frame.add(self.draw_tools)
		
		
		self.draw_table = gtk.Table(rows=8, columns=2, homogeneous=False)
		self.draw_table.attach(gtk.Label("Average: "),0,1,0,1)
		self.draw_table.attach(gtk.Label(draw.average),1,2,0,1)
		
		self.draw_table.attach(gtk.Label("Median: "),0,1,1,2)
		self.draw_table.attach(gtk.Label(draw.median),1,2,1,2)
		
		self.draw_table.attach(gtk.Label("SD: "),0,1,2,3)
		self.draw_table.attach(gtk.Label(draw.sd),1,2,2,3)
		
		self.draw_table.attach(self.draw_adj_frame,0,2,3,4)
		
		self.mime_tools = gtk.Table(rows = 4, columns = 2, homogeneous = False)
		self.mime_tools.attach(gtk.Label("Average"),0,2,0,1)
		self.mime_tools.attach(self.mslider3,0,2,1,2)
		
		self.mime_tools.attach(gtk.Label("Distribution"),0,2,2,3)
		self.mime_tools.attach(self.mslider4,0,2,3,4)
		
		self.mime_adj_frame = gtk.Frame(label = "Adjustments")
		self.mime_adj_frame.add(self.mime_tools)
		
		
		self.mime_table = gtk.Table(rows=8, columns=2, homogeneous=False)
		self.mime_table.attach(gtk.Label("Average: "),0,1,0,1)
		self.mime_table.attach(gtk.Label(mime.average),1,2,0,1)
		
		self.mime_table.attach(gtk.Label("Median: "),0,1,1,2)
		self.mime_table.attach(gtk.Label(mime.median),1,2,1,2)
		
		self.mime_table.attach(gtk.Label("SD: "),0,1,2,3)
		self.mime_table.attach(gtk.Label(mime.sd),1,2,2,3)
		
		self.mime_table.attach(self.mime_adj_frame,0,2,3,4)
		
		
		self.reset = gtk.Button("reset")
		self.reset.connect("clicked",self.reset_adjustments)
		
		self.canvas = FigureCanvas(fig)
		self.mpltools = NavigationToolbar(self.canvas,self.window)
	
		self.draw_frame = gtk.Frame(label = "Draw data")
		self.draw_frame.add(self.draw_table)
		
		self.mime_tools = gtk.VBox()
		
		
		self.mime_frame = gtk.Frame(label = "Mime settings")
		self.mime_frame.add(self.mime_table)

		self.side = gtk.VBox()
		self.side.pack_start(self.draw_frame)
		self.side.pack_start(self.mime_frame)

		
		self.side.pack_start(self.reset)

		self.hbox = gtk.HBox()
		self.hbox.pack_start(self.canvas)
		self.hbox.pack_start(self.side,False,False,20)

		self.lbox = gtk.VBox()
		self.lbox.pack_start(self.hbox)
		self.lbox.pack_start(self.mpltools,False,False)
		
		self.window.add(self.lbox)
		self.window.show_all()
		self.window.connect("destroy",self.destroy)
	def main(self):
		gtk.main()

class data:
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


fig = Figure(figsize=(5,4), dpi = 100)
plt = fig.add_subplot(111)

draw = data("draw",'green')
mime = data("mime",'blue')

def plot_draw(x):
	return mlab.normpdf(x,draw.average+base.avgDraw,draw.sd+base.sdDraw)
def plot_mime(x):
	return mlab.normpdf(x,mime.average+base.avgMime,mime.sd+base.sdMime)


def make_plot():
	plt.clear()
	x = linspace(0,largest(),100)
	y = plot_draw(x)
	z = plot_mime(x)
	plt.plot(x,y,x,z)
	plt.grid(True)
	fig.canvas.draw()
	
gobject.idle_add(make_plot)

if __name__ == "__main__":
	base = Base()
	base.main()
	

