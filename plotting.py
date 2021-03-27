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
