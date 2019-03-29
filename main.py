#!/usr/bin/env python3

'''
#####################################################################################
		#Added by the magnificent omarcartera to allow plotting
		self.tfPlot = QtGui.QVBoxLayout(self.tfWidget)
		self.tfPlot.setObjectName(_fromUtf8("tfLayout"))
		#############################################################

		#Added by the magnificent omarcartera to allow plotting
		self.circlePlot = QtGui.QVBoxLayout(self.circleWidget)
		self.circlePlot.setObjectName(_fromUtf8("circleLayout"))
		#############################################################
######################################################################################
'''

'''
::: TO DO :::
1- Put zeros by left click, poles by right click.
6- Remove them by mouse
4- CTRL + Z to remove the most recent zero/pole

2- Move them by mouse, but also keep the analog moving.
3- convert analog movement to keyboard arrows.
5- more decent zero/pole file.
6- go to a better representation than
'''

######################################################################################
import design
import os
import sys
import time

from scipy.signal import *
import scipy.io.wavfile as WAV

import numpy as np
from numpy import interp

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.uic import loadUiType
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QThread, SIGNAL

import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

from scipy.signal import *

from  matplotlib import patches
from matplotlib.figure import Figure
from matplotlib import rcParams

# for keyboard keystrokes detection
from pynput import keyboard

# threading
import _thread
######################################################################################


# :::TESTING TO UPDATE THE PLOT FROM A QT THREAD ::: #

# a thread to update the plot without blocking the GUI (make it crash)
class plotting_thread(QtCore.QThread):
	def __init__(self):
		super(plotting_thread, self).__init__()


	def run(self):
		# self.emit(SIGNAL('observer()'))

		while(1):
			try:
				# call a fuction from the main thread
				self.emit(SIGNAL('observer()'))

				QThread.msleep(300)

			except(TypeError):
				pass


## Speaking of which
class mainApp(QtGui.QMainWindow, design.Ui_MainWindow):
	def __init__(self):
		super(mainApp, self).__init__()
		self.setupUi(self)
		
		# configuring the plotting thread
		self.plotting_thread = plotting_thread()
		self.connect(self.plotting_thread, SIGNAL('observer()'), self.observer)

		self.plotting_thread.start()


		## defining the buttons and connecting them to their functions (handlers)
		self.btn_browse.clicked.connect(self.btn_browse_txt)
		self.btn_clear.clicked.connect(self.btn_clear_fn)
		self.btn_zero.clicked.connect(self.btn_add_zero_fn)
		self.btn_pole.clicked.connect(self.btn_add_pole_fn)

		self.btn_up.clicked.connect(self.btn_up_fn)
		self.btn_down.clicked.connect(self.btn_down_fn)
		self.btn_right.clicked.connect(self.btn_right_fn)
		self.btn_left.clicked.connect(self.btn_left_fn)

		self.btn_ok.clicked.connect(self.btn_ok_fn)


		## defining global variables for saving zeros and poles
		self.zeros_real = []
		self.zeros_img = []
		
		self.poles_real = []
		self.poles_img = []
		

		## variables used to move zeros and poles
		self.drag = 0
		self.anhy = ' '
		self.accuracy = 0.01

		self.lnd_accuracy.setText(str(self.accuracy))


		## setting minimum distance between mouse click and either a zero or a pole
		self.dist = 0.05


		## the zeros (a) and the poles (b) that will be converted to a transfer function
		self.a_sum = []
		self.b_sum = []


		## x and y coordinates of the mouse
		self.xPoint = 0
		self.yPoint = 0
		
		
		## cleaning the whole thing before running the code for the first time
		self.btn_clear_fn()

		# start the thread to listen for keyboard presses
		_thread.start_new_thread(self.listener_fn, ())

		# _thread.start_new_thread(self.observer, ())

		self.ls = []
		self.undo_stack = []
		self.redo_stack = []

		self.temp_z = -1
		self.temp_p = -1


	def observer(self):
		changed = False

		if self.temp_z < len(self.zeros_real):
			print('zero was added!')
			self.temp_z = len(self.zeros_real)
			changed = True

		elif self.temp_z > len(self.zeros_real):
			print('zero was removed!')
			self.temp_z = len(self.zeros_real)
			changed = True

		if self.temp_p < len(self.poles_real):
			print('pole was added!')
			self.temp_p = len(self.poles_real)
			changed = True

		elif self.temp_p > len(self.poles_real):
			print('pole was removed!')
			self.temp_p = len(self.poles_real)
			changed = True

		if changed:
			self.drawCircle()
			self.btn_draw_tf_fn()


		self.temp_z = len(self.zeros_real)
		self.temp_p = len(self.poles_real)


	## the functions that handles the click of the mouth
	def on_mouse_click(self, event):
		pressed_button = event.button

		## acquiring the mouse click position
		ix, iy = float(event.xdata), float(event.ydata)
		self.xPoint, self.yPoint = ix, iy
		

		## hold ctrl with mouse press to remove zeros/poles
		if (self.ls == ['Key.ctrl']):
			for i in range(0, len(self.zeros_real)):
				distance = ((self.xPoint - self.zeros_real[i])**2 + (abs(self.yPoint) - self.zeros_img[i])**2) **.5
				if (distance <= self.dist):
					del self.zeros_real[i]
					del self.zeros_img[i]



			for i in range(0, len(self.poles_real)):
				distance = ((self.xPoint - self.poles_real[i])**2 + (abs(self.yPoint) - self.poles_img[i])**2) **.5
				if (distance <= self.dist):
					del self.poles_real[i]
					del self.poles_img[i]


		## left click to add zeros, adding them to the arrays
		elif (pressed_button == 1):            
			self.zeros_real.append(ix)
			self.zeros_img.append(iy)

			self.undo_stack.append('z')


		## right click to add poles, adding them to the arrays
		elif (pressed_button == 3):
			self.poles_real.append(ix)
			self.poles_img.append(iy)
			
			self.undo_stack.append('p')


		## if the user has entered 'm' we will start the moving procedures
		elif ('s' == 'm'):
			for i in range(0, len(self.zeros_real)):
				distance = ((self.xPoint - self.zeros_real[i])**2 + (self.yPoint - self.zeros_img[i])**2) **.5
				if (distance <= self.dist):
					self.drag = i
					self.anhy = 'z'

			for i in range(0, len(self.poles_real)):
				distance = ((self.xPoint - self.poles_real[i])**2 + (self.yPoint - self.poles_img[i])**2) **.5
				if (distance <= self.dist):
					self.drag = i
					self.anhy = 'p'


		else:
			print ("Error")



	def on_mouse_release(self, event):
		pass


	def listener_fn(self):
		with keyboard.Listener(self.on_keyboard_press, self.on_keyboard_release) as listener:
			listener.join()


	# what to do when the buttons combination is pressed
	def on_keyboard_press(self, key):
		key = str(key)
		z = '\'z\''
		y = '\'y\''


		if key in ['Key.ctrl', z, y]:
			print('yes')
			self.ls.append(str(key))

		if sorted(self.ls) == sorted(['Key.ctrl', z]):
			self.undo()

		if sorted(self.ls) == sorted(['Key.ctrl', y]):
			self.redo()


	# undo the most recent zero/pole action
	def undo(self):
		temp = self.undo_stack.pop()
		self.redo_stack.append(temp)

		if(temp == 'z'):
			self.zeros_real.pop()
			self.zeros_img.pop()

		else:
			self.poles_real.pop()
			self.poles_img.pop()


	# redo the undoed action(s)
	def redo(self):
		# logic is not consistent yet
		print('redoing')

		temp = self.redo_stack.pop()

		self.undo_stack.append(temp)

		if(temp == 'z'):
			self.zeros_real.pop()
			self.zeros_img.pop()

		else:
			self.poles_real.pop()
			self.poles_img.pop()


	# what to do when the buttons combination is released .. ahem
	def on_keyboard_release(self, key):
		key = str(key)
		z = '\'z\''
		y = '\'y\''

		if key in ['Key.ctrl', z, y]:
			self.ls.remove(str(key))	
		

	## clearing any given plot. Courtsey: Mahmoud Fathy
	def clearLayout(self, layout):
		for i in reversed(range(layout.count())):
			item = layout.itemAt(i)

			if isinstance(item, QtGui.QWidgetItem):
				#print "widget" + str(item)
				item.widget().close()
				# or
				# item.widget().setParent(None)
			elif isinstance(item, QtGui.QSpacerItem):
				k=0
				#print "spacer " + str(item)
				# no need to do extra stuff
			else:
				#print "layout " + str(item)
				self.clearLayout(item.layout())

			# remove the item from layout
			layout.removeItem(item)



	## browsing a .txt file to read it
	def btn_browse_txt(self):

		## clearing the content of our zeros and poles to draw only the tf of the file
		self.zeros_real = []
		self.zeros_img = []
		
		self.poles_real = []
		self.poles_img = []


		## settings to see only .txt files
		## the zeros and poles are in the form: zr0.5 .. zi0.4 .. pr0.7 .. pi0.1
		filePath = QtGui.QFileDialog.getOpenFileNames(self, 'Choose a text file', "/home/omarcartera/Desktop", '*.txt')
		
		fileHandle = open(filePath[0], 'r')
		lines = fileHandle.readlines()
		for line in lines:
			if line[0] == 'z':
				if line[1] == 'r':
					self.zeros_real.append(float(line[2:]))


				elif line[1] == 'i':
					self.zeros_img.append(float(line[2:]))

				else:
					print("Error")

				self.undo_stack.append('z')



			elif line[0] == 'p':
				if line[1] == 'r':
					self.poles_real.append(float(line[2:]))


				elif line[1] == 'i':
					self.poles_img.append(float(line[2:]))

				else:
					print("Error")

				self.undo_stack.append('p')



	## clearing every single character in the code, returning everything to its initial condition
	def btn_clear_fn(self):

		self.zeros_real = []
		self.zeros_img = []
		
		self.poles_real = []
		self.poles_img = []
		
		self.a_sum = []
		self.b_sum = []

		self.accuracy = 0.01
		self.lnd_accuracy.setText(str(self.accuracy))
		
		self.clearLayout(self.tfPlot)
		self.clearLayout(self.circlePlot)
		


	## used to draw any figure, reducing program memory computation
	def draw(self, fig, which):
		self.canvas = FigureCanvas(fig)

		if which == 0:
			self.circlePlot.addWidget(self.canvas)

		if which == 1:
			self.tfPlot.addWidget(self.canvas)

		self.canvas.draw()    


	## drawing an updated circle with its zeros and poles on it
	def drawCircle(self):
		
		self.clearLayout(self.circlePlot)
		angle = np.linspace(-1 * np.pi, np.pi, 1000)
		
		xp = np.cos(angle)
		yp = np.sin(angle)
		
		self.fig1 = Figure()
		self.fig1.patch.set_facecolor('white')
		self.ax1f1 = self.fig1.add_subplot(111)
		self.ax1f1.plot(xp, yp)

		## remove the loop
		for i in range(0, len(self.zeros_real)):
			self.ax1f1.plot(self.zeros_real[i], self.zeros_img[i], 'go', markersize = 9, alpha = 1.0)
			self.ax1f1.plot(self.zeros_real[i], - self.zeros_img[i], 'go', markersize = 9, alpha = 1.0)

		for i in range(0, len(self.poles_real)):
			self.ax1f1.plot(self.poles_real[i], self.poles_img[i], 'rx', markersize = 9, alpha = 1.0) ## makan el poles
			self.ax1f1.plot(self.poles_real[i], - self.poles_img[i], 'rx', markersize = 9, alpha = 1.0) ## makan el poles


		self.ax1f1.spines['left'].set_position('center')
		self.ax1f1.spines['bottom'].set_position('center')
		self.ax1f1.spines['right'].set_visible(False)
		self.ax1f1.spines['top'].set_visible(False)
	
		self.ax1f1.grid()
		
		self.draw(self.fig1, 0)
		
		self.fig1.canvas.mpl_connect('button_press_event', self.on_mouse_click)
		self.fig1.canvas.mpl_connect('button_release_event', self.on_mouse_release)


	## used to add zeros by hand
	def btn_add_zero_fn(self):
		self.zeros_real.append(float(self.lnd_zero_real.text()))
		self.zeros_img.append(float(self.lnd_zero_img.text()))
		
		self.undo_stack.append('z')

		self.lnd_zero_real.clear()
		self.lnd_zero_img.clear()
		


	## used to add poles by hand
	def btn_add_pole_fn(self):
		self.poles_real.append(float(self.lnd_pole_real.text()))
		self.poles_img.append(float(self.lnd_pole_img.text()))

		self.undo_stack.append('p')

		self.lnd_pole_real.clear()
		self.lnd_pole_img.clear()
	


	## moving a specific point up in the imaginary axis
	def btn_up_fn(self):
		if self.anhy == 'z':
			self.zeros_img[self.drag] = self.zeros_img[self.drag] + float(self.lnd_accuracy.text())
			

		elif self.anhy == 'p':
			self.poles_img[self.drag] = self.poles_img[self.drag] + float(self.lnd_accuracy.text())


	## moving a specific point down in the imaginary axis
	def btn_down_fn(self):
		if self.anhy == 'z':
			self.zeros_img[self.drag] = self.zeros_img[self.drag] - float(self.lnd_accuracy.text())


		elif self.anhy == 'p':
			self.poles_img[self.drag] = self.poles_img[self.drag] - float(self.lnd_accuracy.text())



	## moving a specific point uright in the real axis
	def btn_right_fn(self):
		if self.anhy == 'z':
			self.zeros_real[self.drag] = self.zeros_real[self.drag] + float(self.lnd_accuracy.text())


		elif self.anhy == 'p':
			self.poles_real[self.drag] = self.poles_real[self.drag] + float(self.lnd_accuracy.text())


	## moving a specific point left in the real axis
	def btn_left_fn(self):
		if self.anhy == 'z':
			self.zeros_real[self.drag] = self.zeros_real[self.drag] - float(self.lnd_accuracy.text())


		elif self.anhy == 'p':
			self.poles_real[self.drag] = self.poles_real[self.drag] - float(self.lnd_accuracy.text())



	## release the point that we are holding and dragging
	def btn_ok_fn(self):
		self.drag = []
		self.anhy = ' '

		self.accuracy = 0.01
		self.lnd_accuracy.setText(str(self.accuracy))


	## drawing the transfer function of any filter is made down here
	def btn_draw_tf_fn(self):
		
		## clearing the arrays
		self.a_sum = []
		self.b_sum = []

		## clearing the plot space
		self.clearLayout(self.tfPlot)
		
		
		## appending all the zeros and poles into the a and b arrays
		for avada in range(0, len(self.zeros_real)):
			self.a_sum.append(complex(self.zeros_real[avada], self.zeros_img[avada]))
			self.a_sum.append(complex(self.zeros_real[avada], -self.zeros_img[avada]))
			
			
		for kedavra in range(0, len(self.poles_real)):
			self.b_sum.append(complex(self.poles_real[kedavra], self.poles_img[kedavra]))
			self.b_sum.append(complex(self.poles_real[kedavra], -self.poles_img[kedavra]))
			
		
		
		a = np.array(self.a_sum)
		b = np.array(self.b_sum)

		
		## getting the num and den of the tf
		(NumeratorZcoefs, DenominatorZcoefs) = zpk2tf(a, b, 1)

		## getting the frequency response of a given num/den
		FreqResponse = freqz(NumeratorZcoefs, DenominatorZcoefs)
			
		self.fig2 = Figure()
		self.fig2.patch.set_facecolor('white')
		self.ax1f2 = self.fig2.add_subplot(111)
		self.ax1f2.plot(FreqResponse[0], abs(np.array(FreqResponse[1])))
		
		self.ax1f2.set_xlim(0, np.pi)
		
		self.draw(self.fig2, 1)




def main():
	App = QtGui.QApplication(sys.argv)
	form = mainApp()
	form.show()
	App.exec_()

	
if __name__ == '__main__':
	main()