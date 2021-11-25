import csv
import sys

import matplotlib.pyplot as plt


class BenchmarkReport:
	def __init__(self, sizes: list, bench_map: dict):
		self.sizes = sizes
		self.bench_map = bench_map


def parse_benchmark_report(file_path: str) -> BenchmarkReport:
	report = BenchmarkReport(sizes = [], bench_map = { })

	with open(file_path) as file:
		reader = csv.DictReader(file)

		prev_size = -1
		for line in reader:
			size = int(line['Size'])
			if size != prev_size:
				report.sizes.append(size)
				prev_size = size

			method_name = line['Method']
			if method_name in report.bench_map:
				report.bench_map[method_name].append(float(line['Mean']))
			else:
				report.bench_map[method_name] = [float(line['Mean'])]

	return report


if __name__ == '__main__':
	report = parse_benchmark_report(file_path = sys.argv[1])

	plot_lines = []
	for method in report.bench_map.keys():
		plot_lines += plt.plot(report.sizes, report.bench_map[method])

	plt.legend(plot_lines, report.bench_map.keys())
	plt.show()
