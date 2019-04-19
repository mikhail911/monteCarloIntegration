import random
import sys
import time

import numpy as np
import pyqtgraph as pg
from Equation import Expression
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets

class MonteCarlo(QtGui.QMainWindow):
	def __init__(self, int_func, xmin, xmax, ymin, N, parent=None):
		super(MonteCarlo, self).__init__(parent)
		self.x_min = xmin
		self.x_max = xmax
		self.y_min = ymin
		self.int_func = int_func
		self.x = np.linspace(self.x_min, self.x_max, 1000)
		self.y_max = max(self.integral_function(self.x)) + 0.1 * max(self.integral_function(self.x))
		self.n = N
		self.first_lines = True
		self.xmin_line = ''
		self.xmax_line = ''
		self.ymin_line = ''
		self.ymax_line = ''

		pg.setConfigOption('background', 'w')
		pg.setConfigOption('antialias', True)
		self.setWindowIcon(QtGui.QIcon('monteCarloIcon.png'))
		self.setWindowTitle('Monte Carlo Integration')
		self.setGeometry(50, 50, 860, 640)
		self.setStyleSheet("font-family: New Century Schoolbook; font-size: 16px")

		self.mainbox = QtGui.QWidget()
		self.mainbox.setLayout(QtGui.QVBoxLayout())
		self.fuction_layout = QtGui.QWidget()
		self.fuction_layout.setLayout(QtGui.QGridLayout())
		self.options_layout = QtGui.QWidget()
		self.options_layout.setLayout(QtGui.QHBoxLayout())
		self.setCentralWidget(self.mainbox)

		# Options first row
		self.f_label = QtGui.QLabel('<i>f(x)</i> = ')
		self.f_input = QtGui.QLineEdit()
		self.f_input.setText(str(self.int_func))
		self.f_input.textChanged.connect(self.current_function_change)
		self.help_button = QtGui.QPushButton()
		self.help_button.setIcon(QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_TitleBarContextHelpButton))
		self.help_button.clicked.connect(self.show_function_help)
		
		# Options second row
		self.xmin_label = QtGui.QLabel('<i>x<sub>min</sub></i> = ')
		self.xmin_input = QtGui.QLineEdit()
		self.xmin_input.setText(str(float(self.x_min)))
		self.xmin_input.setValidator(QtGui.QDoubleValidator(0.99, 99.99, 2))
		self.xmin_input.textChanged.connect(self.current_xmin_change)

		self.xmax_label = QtGui.QLabel('<i>x<sub>max</sub></i> = ')
		self.xmax_input = QtGui.QLineEdit()
		self.xmax_input.setText(str(float(self.x_max)))
		self.xmax_input.setValidator(QtGui.QDoubleValidator(0.99, 99.99, 2))
		self.xmax_input.textChanged.connect(self.current_xmax_change)
		
		self.ymin_label = QtGui.QLabel('<i>y<sub>min</sub></i> = ')
		self.ymin_input = QtGui.QLineEdit()
		self.ymin_input.setValidator(QtGui.QDoubleValidator(0.99, 99.99, 2))
		self.ymin_input.setText(str("{0:.2f}".format(float(self.y_min))))
		self.ymin_input.textChanged.connect(self.current_ymin_change)

		self.ymax_label = QtGui.QLabel('<i>y<sub>max</sub></i> = ')
		self.ymax_input = QtGui.QLineEdit()
		self.ymax_input.setEnabled(False)
		self.ymax_input.setValidator(QtGui.QDoubleValidator(0.99, 99.99, 2))
		self.ymax_input.setText(str("{0:.2f}".format(float(self.y_max))))

		self.draw_button = QtGui.QPushButton()
		self.draw_button.setText('Draw')
		self.draw_button.clicked.connect(self.get_function)

		# Options third row
		self.n_label = QtGui.QLabel()
		self.n_label.setText('<i>N</i> = ')
		self.n_select = QtGui.QComboBox()
		self.n_select.addItems(['100', '1000', '10000', '100000'])
		self.n_select.currentTextChanged.connect(self.change_n)
		self.stop_button = QtGui.QPushButton('Stop')
		self.stop_button.setEnabled(False)
		self.calc_button = QtGui.QPushButton('Calculate')
		self.calc_button.clicked.connect(self.monte_carlo)

		self.fuction_layout.layout().addWidget(self.f_label, 0, 0, 1, 1)
		self.fuction_layout.layout().addWidget(self.f_input, 0, 1, 1, 7)
		self.fuction_layout.layout().addWidget(self.help_button, 0, 8, 1, 1)
		self.fuction_layout.layout().addWidget(self.xmin_label, 1, 0, 1, 1)
		self.fuction_layout.layout().addWidget(self.xmin_input, 1, 1, 1, 1)
		self.fuction_layout.layout().addWidget(self.xmax_label, 1, 2, 1, 1)
		self.fuction_layout.layout().addWidget(self.xmax_input, 1, 3, 1, 1)
		self.fuction_layout.layout().addWidget(self.ymin_label, 1, 4, 1, 1)
		self.fuction_layout.layout().addWidget(self.ymin_input, 1, 5, 1, 1)
		self.fuction_layout.layout().addWidget(self.ymax_label, 1, 6, 1, 1)
		self.fuction_layout.layout().addWidget(self.ymax_input, 1, 7, 1, 1)
		self.fuction_layout.layout().addWidget(self.draw_button, 1, 8, 1, 1)
		self.fuction_layout.layout().addWidget(self.n_label, 2, 0, 1, 1)
		self.fuction_layout.layout().addWidget(self.n_select, 2, 1, 1, 1)
		self.fuction_layout.layout().addWidget(self.stop_button, 2, 4, 1, 2)
		self.fuction_layout.layout().addWidget(self.calc_button, 2, 6, 1, 3)
		
		self.canvas = pg.GraphicsLayoutWidget()
		self.status_bar = QtWidgets.QStatusBar()
		self.status_bar.showMessage(' ')
		self.mainbox.layout().addWidget(self.fuction_layout)
		self.mainbox.layout().addWidget(self.canvas)   
		self.setStatusBar(self.status_bar) 

		self.otherplot = self.canvas.addPlot()
		self.h2 = self.otherplot.plot(pen='#000000')
		self.h3 = self.otherplot.plot(pen='r')
		self.h4 = self.otherplot.plot(pen='g')

		self.redraw_function()
	
	def redraw_function(self):
		self.y_max = self.calculate_ymax()
		self.y = self.integral_function(self.x)
		
		if self.first_lines is False:
			self.otherplot.removeItem(self.xmin_line)
			self.otherplot.removeItem(self.xmax_line)
			self.otherplot.removeItem(self.ymin_line)
			self.otherplot.removeItem(self.ymax_line)
		
		self.xmin_line = pg.InfiniteLine(pos=self.x_min, angle = 90, movable = False, pen = pg.mkPen('#FF8C00', width = 1, style = QtCore.Qt.DashLine))
		self.xmax_line = pg.InfiniteLine(pos=self.x_max, angle = 90, movable = False, pen = pg.mkPen('#FF8C00', width = 1, style = QtCore.Qt.DashLine))
		self.ymin_line = pg.InfiniteLine(pos=self.y_min, angle = 0, movable = False, pen = pg.mkPen('#FF8C00', width = 1, style = QtCore.Qt.DashLine))
		self.ymax_line = pg.InfiniteLine(pos=self.y_max, angle = 0, movable = False, pen = pg.mkPen('#FF8C00', width = 1, style = QtCore.Qt.DashLine))
		
		self.h2.setData(self.x, self.y, pen = pg.mkPen('b', width = 3))		
		self.otherplot.addItem(self.xmin_line)
		self.otherplot.addItem(self.xmax_line)
		self.otherplot.addItem(self.ymin_line)
		self.otherplot.addItem(self.ymax_line)
		self.otherplot.showGrid(x = True, y = True)
		self.first_lines = False
		pg.QtGui.QApplication.processEvents()

	def integral_function(self, x): 
		y = Expression(self.int_func, ['x'])
		return(y(x))
	
	def current_function_change(self, new_func):
		self.int_func = new_func

	def current_xmin_change(self, xmin):
		self.x_min = float(xmin.replace(',','.'))

	def current_xmax_change(self, xmax):
		self.x_max = float(xmax.replace(',','.'))

	def current_ymin_change(self, ymin):
		self.y_min = float(ymin.replace(',','.'))

	def get_function(self):
		try:
			self.int_func = Expression(self.int_func, ['x'])
			self.redraw_function()
		except TypeError as t:
			QtGui.QMessageBox.critical(self, "Monte Carlo Error", 'Error: '+str(t)+"", QtGui.QMessageBox.Ok)

	def change_n(self, new_n):
		self.n = int(new_n)

	def calculate_ymax(self):
		ymax = max(self.integral_function(self.x)) + 0.1 * max(self.integral_function(self.x))
		self.ymax_input.setText(str("{0:.2f}".format(float(self.y_max))))
		return(ymax)
	
	def _update(self, x_list, y_list, r):
		if r is True:
			self.h3.setData(x_list, y_list, pen = None, symbol = 'o', symbolPen = None, symbolSize = 4, symbolBrush = ('r'))
		else:
			self.h4.setData(x_list, y_list, pen = None, symbol = 'o', symbolPen = None, symbolSize = 4, symbolBrush = ('g'))
		pg.QtGui.QApplication.processEvents()

	def monte_carlo(self):
		whole_area = (self.x_max - self.x_min) * (self.y_max - self.y_min)
		points = 0 
		time_start = time.time()

		x_list_r = list()
		y_list_r = list()
		x_list_g = list()
		y_list_g = list()

		for i in range(self.n):
			x = self.x_min + (self.x_max - self.x_min) * random.random()
			y = self.y_min + (self.y_max - self.y_min) * random.random()
			
			if y > 0 and y <= self.integral_function(x):
				points += 1
				x_list_g.append(x)
				y_list_g.append(y)
				self._update(x_list_g, y_list_g, False)
			elif y < 0 and y >= self.integral_function(x):
				x_list_g.append(x)
				y_list_g.append(y)
				self._update(x_list_g, y_list_g, False)
			elif y > self.integral_function(x):
				#points_bad += 1
				x_list_r.append(x)
				y_list_r.append(y)
				self._update(x_list_r, y_list_r, True)
			self.status_bar.showMessage('Current point: {0} out of {1}'.format(("{0:,}".format(i)).replace(",", " "), ("{0:,}".format(self.n)).replace(",", " ")))

		time_stop = time.time()
		total_time = time_stop - time_start
		result = whole_area * (points) / self.n
	
		self.status_bar.showMessage('Result: {0}, Total time: {1} [s], N: {2}'.format(result, total_time, "{0:,}".format(self.n).replace(",", " ")))
		return {'result': result, 'time': total_time, 'N': N}
	
	def show_function_help(self):
		info_box = QtGui.QMessageBox(self)
		info_box.setIcon(QtGui.QMessageBox.Information)
		info_box.setWindowTitle('Monte Carlo Integration - Functions Info')
		info_box.setText('Functions compatibile with app: <br> \
		&nbsp;&nbsp;&nbsp;&nbsp;- abs(x), sin(x), cos(x), tan(x), re(x), im(x), sqrt(x) <br><br> \
		Constants compatibile with app: <br> \
		&nbsp;&nbsp;&nbsp;&nbsp;- pi, e, h (Plancks Constant), c (Speed of Light)  <br><br> \
		For full reference, look here: <br> \
		<center><a href="https://github.com/glenfletcher/Equation/blob/master/doc/source/Functions.rst">Link</a></center><br><br> \
		')
		info_box.setTextFormat(QtCore.Qt.TextFormat(QtCore.Qt.RichText))
		info_box.exec_()

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	function = 'e^(-x)'
	xmin = 0
	xmax = 10
	ymin = 0
	N = 100

	thisapp = MonteCarlo(function, xmin, xmax, ymin, N)
	thisapp.show()
	sys.exit(app.exec_())
