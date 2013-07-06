import math
#import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use('WXAgg')
mpl.interactive(False)

import pylab as pl
from pylab import get_current_fig_manager as gcfm
import wx
import numpy as np
import random

def is_number(val):
    try:
        int(val)
        return True
    except ValueError:
        return False

#Function to get week number
def getWeekNumber(releaseDate):
	if not is_number(releaseDate[0]):
		return False
	month=releaseDate[1].lower()
	#Finding total days passed previous month of release dates month
	if month=="jan" or month=="january":
		days=0
	elif month=="feb" or month=="february":
		days=31
	elif month=="mar" or month=="march":
		days=59
	elif month=="apr" or month=="april":
		days=90
	elif month=="may":
		days=120
	elif month=="jun" or month=="june":
		days=151
	elif month=="jul" or month=="july":
		days=181
	elif month=="aug" or month=="august":
		days=222
	elif month=="sep" or month=="september":
		days=253
	elif month=="oct" or month=="october":
		days=283
	elif month=="nov" or month=="november":
		days=314
	elif month=="dec" or month=="december":
		days=334
	else:
		return False

	if is_number(releaseDate[2]):
		year = int(releaseDate[2])
		#Adding a day to days if release year is leap year and month is after feb
		if year%4==0 and month!="jan" and month!="january" and month!="feb" and month!="february":
			days+=1
	days+=int(releaseDate[0])
	return int(math.ceil(days/7.0))
	

movieDataFile=open('movieData.list','r')
#Creating list for data
aggregatedData=[]
for i in xrange(0,52):
	weeklyData={}
	weeklyData['totalRatings']=0.0
	weeklyData['numberOfRatings']=0
	weeklyData['minRating']=10
	weeklyData['maxRating']=0
	aggregatedData.append(weeklyData)

while True:
	dataLine=movieDataFile.readline().rstrip("\n")
	#Monitoring end of file
	if dataLine=="":
		break
	dataLine=dataLine.split("attribute:")
	rating=dataLine[2]
	releaseDate=dataLine[3]
	releaseDate=releaseDate.split(" ")
	if len(releaseDate)<3:
		continue
	week=getWeekNumber(releaseDate)
	if week==False:
		continue
	if week==53:
		week=52
	#Adding data to respective list
	aggregatedData[week-1]['totalRatings']+=float(rating)
	aggregatedData[week-1]['numberOfRatings']+=1
	if aggregatedData[week-1]['minRating']>float(rating):
		aggregatedData[week-1]['minRating']=float(rating)
	if aggregatedData[week-1]['maxRating']<float(rating):
		aggregatedData[week-1]['maxRating']=float(rating)

movieDataFile.close()
#Finding average ratings
average=[0]*52
for i in xrange(0,52):
	if aggregatedData[i]['numberOfRatings']==0:
		average[i]=0
		continue
	average[i]=aggregatedData[i]['totalRatings']/aggregatedData[i]['numberOfRatings']

#Plotting graph
class wxToolTipExample(object):
	def __init__(self):
		#Setting properties of graph
		self.figure = pl.figure()
		self.axis = self.figure.add_subplot(111)
		self.tooltip = wx.ToolTip(tip='')
		gcfm().canvas.SetToolTip(self.tooltip)
		self.tooltip.Enable(False)
		self.tooltip.SetDelay(0)
		self.figure.canvas.mpl_connect('button_press_event', self._onClick)
		self.figure.canvas.mpl_connect('motion_notify_event', self._onMotion)
		self.dataX = range(1,53)
		self.dataY = average
		self.axis.set_xlabel('Weeks')
		self.axis.set_ylabel('Ratings')
		self.axis.plot(self.dataX, self.dataY, linestyle='-', marker='o', markersize=10, label='ratingsPlot')

	def _onClick(self, event):
		if event.xdata != None and event.ydata != None: # mouse is inside the axes
			#Monitoring Clicks on data point
			currentX=event.xdata
			floor=math.floor(currentX)
			ceil=math.ceil(currentX)
			if currentX-floor>ceil-currentX:
				currentX=ceil
			else:
				currentX=floor
			if currentX<1 or currentX>52:
				top = tip=' '
				self.tooltip.SetTip(tip) 
				self.tooltip.Enable(True)
				return
			yData=self.dataY[int(currentX)-1]
			currentY= event.ydata
			if currentY+0.02>yData and currentY-0.02<yData:
				currentY=currentX
			else:
				top = tip=''
				self.tooltip.SetTip(tip) 
				self.tooltip.Enable(True)
				return
			#Setting tooltip
			top = tip='Week Number:%s\nAverage Rating:%.2f\nNumber of Releases:%s\nLowest Rating:%s\nHighest Rating:%s' %(int(currentX),average[int(currentX)-1],aggregatedData[int(currentX)-1]['numberOfRatings'],aggregatedData[int(currentX)-1]['minRating'],aggregatedData[int(currentX)-1]['maxRating'])
			self.tooltip.SetTip(tip) 
			self.tooltip.Enable(True)
	
	def _onMotion(self, event):
		#Unsetting tooltip on mouse move
		top = tip=' '
		self.tooltip.SetTip(tip) 
		self.tooltip.Enable(True)
		return



example = wxToolTipExample()
pl.show()
