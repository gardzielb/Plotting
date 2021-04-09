import csv
from typing import List, Tuple

import numpy as np


class MeasureSeries:
	def __init__( self ):
		self.data = []

	def append_measure( self, measure: List[str] ):
		for i in range( len( measure ) ):
			if i >= len( self.data ):
				self.data.append( [] )
			self.data[i].append( float( measure[i].replace( ',', '.' ) ) )


def read_data( file_path: str ) -> MeasureSeries:
	measure_series = MeasureSeries()
	with open( file_path ) as file:
		reader = csv.reader( file )
		for row in reader:
			measure_series.append_measure( row )
	return measure_series


def least_squares( x: List[float], y: List[float], bmult = 0 ) -> Tuple[float, float]:
	a_matrix = np.vstack( [x, bmult * np.ones( len( x ) )] ).T
	a, b = np.linalg.lstsq( a_matrix, y, rcond = None )[0]
	print( f'Least squares result: a = {a}, b = {b}' )
	return a, b


def least_squares_errors( x: List[float], y: List[float], y_error: List[float] ) -> dict:
	x_array = np.array( x )
	y_array = np.array( y )
	w_array = 1 / (np.array( y_error ) ** 2)

	a_up = w_array.sum() * (w_array * x_array * y_array).sum() - (w_array * x_array).sum() * (w_array * y_array).sum()
	a_down = w_array.sum() * (w_array * x_array ** 2).sum() - (x_array * w_array).sum() ** 2
	a = a_up / a_down

	s_down = w_array.sum() * (w_array * x_array ** 2).sum() - (x_array * w_array).sum() ** 2
	s_a = np.sqrt( w_array.sum() / s_down )

	b_up = \
		(w_array * x_array ** 2).sum() * (w_array * y_array).sum() - \
		(w_array * x_array).sum() * (w_array * x_array * y_array).sum()
	b = b_up / a_down

	s_b = np.sqrt( (w_array * x_array ** 2).sum() / s_down )

	print( f'Least squares result: a = {a}, s_a = {s_a}, b = {b}, s_b = {s_b}' )
	return { 'a': a, 'b': b, 's_a': s_a, 's_b': s_b }
