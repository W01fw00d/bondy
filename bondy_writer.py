# -*- coding: utf-8 -*-

import os
import glob
import csv

class BondyWriter:

	def __init__(self):
		type_of_file = '.csv'
		self.text = ''
		inputs = self.getAllInputCSVs()

		for input in inputs:
			self.formatInput(input)

	def getAllInputCSVs(self):
		result = glob.glob('input/*.csv')
		return result

	def formatInput(self, input):
		text_file = open(input, 'r')
		points_line = text_file.readline()
		points_list = points_line.split(",")
		filtered_point_list = filter(None, points_list)

		text_file.readline() #trash header

		data_matrix = []
		#We left an empty item that will convert into an empty cell on the final csv
		wavelength_list = ['']

		for data_line in text_file:
			data_line_list = data_line.split(",")

			try:
				float(data_line_list[0])
			except ValueError:
				#It's not a float, so we will stop here the iteration as we finished reading the data results
				break

			wavelength_list.append(data_line_list.pop(0))

			#get even index items, wich contains useful result data
			data_line_list = data_line_list[::2]
			data_matrix.append(data_line_list)

		#Get the name_of_file.csv, without the path
		file_name = text_file.name.split("\\")[1]

		self.write_formatted_result_into_output_csv(file_name, wavelength_list, filtered_point_list, data_matrix)

		#Debug
		#self.print_formatted_result(wavelength_list, filtered_point_list, data_matrix)

	def write_formatted_result_into_output_csv(self, file_name, wavelength_list, filtered_point_list, data_matrix):
		with open('output/formatted_' + file_name, mode='w') as csv_file:
			results_csv_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

			results_csv_writer.writerow(wavelength_list)

			#interpolate
			line_list = []
			for x in range(len(filtered_point_list) - 1):
				line_list = [filtered_point_list[x]]

				for data_line_list in data_matrix:
					line_list.append(data_line_list[x])

				results_csv_writer.writerow(line_list)

	def print_formatted_result(self, wavelength_list, filtered_point_list, data_matrix):
		print(self.format_list_into_commas_string(wavelength_list))

		#interpolate
		for x in range(len(filtered_point_list) - 1):
			print(filtered_point_list[x] + ';')

			for data_line_list in data_matrix:
				print(data_line_list[x] + ';')

	def format_list_into_commas_string(self, list):
		return ";".join(map(str, list))
