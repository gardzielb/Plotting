import matplotlib.pyplot as plt
import numpy as np
from argparse import ArgumentParser

from Plotter import Plotter
from plotting import read_data, least_squares


def create_arg_parser() -> ArgumentParser:
	parser = ArgumentParser()
	parser.add_argument( '-o', '--output_file', help = 'Specify output file', default = None )
	parser.add_argument( '-c', '--cmp-data', help = 'Input csv file with comparison data', default = None )
	parser.add_argument(
		'-s', '--least-squares', help = 'Match line using least squares method', action = 'store_true'
	)
	parser.add_argument( '-b', '--least-squares-bmult', default = 0 )
	parser.add_argument( '-g', '--grid', help = 'Plot with grid', action = 'store_true' )
	parser.add_argument( '-x', '--xlabel', help = 'X axis label', default = 'x' )
	parser.add_argument( '-y', '--ylabel', help = 'Y axis label', default = 'y' )
	parser.add_argument( '-l', '--labels', help = 'Labels to show in a legend', nargs = '+', default = [] )
	parser.add_argument( 'input_files', metavar = 'input', type = str, nargs = '+', help = 'Input csv files' )
	return parser


if __name__ == '__main__':
	arg_parser = create_arg_parser()
	args = arg_parser.parse_args()

	plotter = Plotter( labels = args.labels, line_fmts = ['-k', ':k', '--k', '-.k'] )

	for path in args.input_files:
		series = read_data( path )
		plotter.plot_with_error( series )
		if args.least_squares:
			x, y = series.data[0], series.data[2]
			a, b = least_squares( x, y, bmult = float( args.least_squares_bmult ) )
			plotter.plot( x, a * np.array( x ) + b )

	if args.cmp_data:
		cmp_series = read_data( args.cmp_data )
		plotter.plot_series( cmp_series )

	if args.grid:
		plt.grid( color = 'k', linestyle = '-', linewidth = 0.3 )

	plt.xlabel( args.xlabel )
	plt.ylabel( args.ylabel )

	if args.labels:
		plt.legend( loc = 'lower right' )
		# plt.legend( loc = 'upper left' )

	if args.output_file:
		plt.savefig( args.output_file )
	else:
		plt.show()
