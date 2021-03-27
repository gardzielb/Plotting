import matplotlib.pyplot as plt
from typing import List

from plotting import MeasureSeries


class Plotter:
	def __init__( self, labels: List[str], line_fmts: List[str] ):
		self.labels = []
		self.labels.extend( labels )
		self.line_fmts = []
		self.line_fmts.extend( line_fmts )
		self.label_index = 0
		self.fmt_index = 0

	def plot_with_error( self, series: MeasureSeries ):
		plt.errorbar(
			series.data[0], series.data[2], xerr = series.data[1], yerr = series.data[3], fmt = '.k', capsize = 2,
			label = self.__get_label__()
		)

	def plot_series( self, series: MeasureSeries ):
		x = series.data[0]
		for i in range( 1, len( series.data ) ):
			plt.plot( x, series.data[i], self.__get_format__(), label = self.__get_label__() )

	def plot( self, x, y ):
		plt.plot( x, y, self.__get_format__(), label = self.__get_label__() )

	def __get_label__( self ):
		if self.labels:
			label = self.labels[self.label_index]
			self.label_index = (self.label_index + 1) % len( self.labels )
			return label
		return ''

	def __get_format__( self ):
		if self.line_fmts:
			fmt = self.line_fmts[self.fmt_index]
			self.fmt_index = (self.fmt_index + 1) % len( self.line_fmts )
			return fmt
		return '-'
