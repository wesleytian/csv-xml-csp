import csv
from itertools import combinations
from sys import argv
from functools import reduce
import operator

f = open('sudoku44_easy.csv')
datafile = open('sudoku44_easy.csv', 'r')
datareader = csv.reader(datafile, delimiter=',')

#create an array to store lines
data = []
#for-each loop (for each line)
for row in datareader: 
	data.append(row)

number_of_variables = int(data[0][0])
number_of_alldiff_constraints = int(data[number_of_variables+1][0])
number_of_nary_constraints = int(data[number_of_variables + number_of_alldiff_constraints + 2][0])

# function that converts rows in data to required xml format
# function for formatting variables and values
def convert_row_variables(row):
	number_of_values = int(row[1]) 
	returnvar = """<VARIABLE TYPE="String">\n\t<NAME>""" + row[0] +"</NAME>\n"
	for i in range(2, number_of_values+2): #print x number of values
		returnvar += "\t<VALUE>" + row[i] + "</VALUE>\n"
	return returnvar + "</VARIABLE>\n"		

# returns the xml code for alldiff constraints 
def convert_alldiff_constraints(combo, row):
	returnvar = """<CONSTRAINT TYPE="Custom">\n\t<CUSTOMNAME>AllDiff</CUSTOMNAME>\n"""
	returnvar += given_combinations(combo) 
	returnvar += "\t<TABLE>" + calculate_truth_table_string(row) + "</TABLE>\n"
	return returnvar + "</CONSTRAINT>\n"

# helper function to print the given names
# generates the <GIVEN> part
def given_combinations(combo):
	returnvar = ""
	for i in range(0, len(combo)):
		returnvar += "\t<GIVEN>" + combo[i] + "</GIVEN>\n" 
	return returnvar

# calculates the truth table string
# helper function for the alldiff constraints function
# generates the <TABLE> part
def calculate_truth_table_string(row):
	count = 0
	for element in row:
		if (element != ''):
			count += 1
	total_values = count ** 2
	table_string = ""
	# print F followed by number of AllDiff constraints - 1 Ts
	# 3 possible values each results in T F F F T F F F T
	# this is a pattern I found. it works for any number of values
	for i in range(0, count-1):
		table_string = table_string + "F "
		for j in range(0, count):
			table_string += "T "
	#print last F
	return table_string + "F"

# generates output formatting for n-ary constraints
def n_ary(row):
	returnvar = """<CONSTRAINT TYPE="CUSTOM">\n<CUSTOMNAME>Untitled Constraint</CUSTOMNAME>\n"""
	returnvar += given_for_n_ary(row)
	returnvar += "\t<TABLE>" + n_ary_constraints(row) + "</TABLE>\n"
	return returnvar + "</CONSTRAINT>\n"

def given_for_n_ary(row):
	arr = []
	for element in row:
		if (element != ''):
			if ("/" in element):
				arr.append(element.split("/"))
				arr.append("not")
			if ("=" in element):
				arr.append(element.split("="))
				arr.append("equal")
	# print(arr)
	given_arr = []
	for item in arr:
		if (item != 'not' and item != 'equal'):
			given_arr.append(item[0])
	returnvar = ""
	for i in range(0, len(given_arr)):
		returnvar += "\t<GIVEN>" + given_arr[i] + "</GIVEN>\n"
	return returnvar

# takes the truth matrix and formats the truth string
def format_matrix(matrix, arr):

	truth_column_size = 1

	# find out truth_column_size
	for col in arr:
		if (col != 'not' and col != 'equal'):
			temp_name = col[0]
			# print(temp_name)
			for j in range(1, number_of_variables + 1):
				if(data[j][0] == temp_name):
					truth_column_size *= int(data[j][1])

	# create truth column
	# truth_column = [None] * truth_column_size

	for i in range(0, len(arr)):

		# put false in truth value where there is a not
		if (arr[i] == 'not'):
			# find the index where the name in the clause is false
			truth_column = ["T"] * truth_column_size

			temp_name = arr[i-1][0]
			for j in range(1, number_of_variables + 1):
				if(data[j][0] == temp_name):
					temp_row = data[j]
					temp_row = temp_row[2:]				
					for k in range(0, len(temp_row)):
						if (arr[i-1][1] == temp_row[k]):
							truth_column[k] = "F"

		# put true in truth value where there is a not
		if (arr[i] == 'equal'):
			# find the index where the name in the clause is true
			truth_column = ["F"] * truth_column_size

			temp_name = arr[i-1][0]
			for j in range(1, number_of_variables + 1):
				if(data[j][0] == temp_name):
					temp_row = data[j]
					temp_row = temp_row[2:]				
					for k in range(0, len(temp_row)):
						if (arr[i-1][1] == temp_row[k]):
							truth_column[k] = "T"



	
	for i in range(0, len(truth_column)):
		if (truth_column[i] == None):
			truth_column[i] = "F"

	# convert truth_column into properly formatted string
	output = ""
	for i in range(0, len(truth_column)):
		output += str(truth_column[i]) + " "
	# remove last space
	return output[0:len(output)-1]

# generates the truth table matrix for n-ary constraints
def n_ary_constraints(row):
	arr = []
	domain_size_arr = []

	# create 2d arr that has the clauses and the constraints separately
	# [['A_pet', 'dog'], 'not', ['A_food', 'chocolate'], 'not']
	for element in row:
		if (element != ''):
			if ("/" in element):
				arr.append(element.split("/"))
				arr.append("not")
			if ("=" in element):
				arr.append(element.split("="))
				arr.append("equal")
	# print(arr)
	for col in arr:
		if(col != 'not' and col != 'equal'):
			# temp_name stores the first clauses name (ex: A_pet)
			temp_name = col[0]
			# loops through variable rows and finds the possible values of temp_name
			for i in range(1, number_of_variables+1):
				if(data[i][0] == temp_name):
					temp_row = data[i]
					temp_row_edited = temp_row[2:]
					domain_size_arr.append(len(temp_row_edited))

	matrix = []

	for col in arr:
		if(col != 'not' and col != 'equal'):
			# temp_name stores the first clauses name (ex: A_pet)
			temp_name = col[0]
			# loops through variable rows and finds the possible values of temp_name
			for i in range(1, number_of_variables+1):
				if(data[i][0] == temp_name):
					# saves the possible values of temp_name in temp_row_edited
					temp_row = data[i]
					temp_row_edited = temp_row[2:]

					# uses helper method to combine columns into a complete truth matrix
					matrix.append(constraints_matrix_helper(temp_row_edited, domain_size_arr))
					#domain_size_arr is local [PROBLEM])
	list(reversed(matrix))
	return format_matrix(matrix, arr)

# helper function to fill in the truth table matrix
def constraints_matrix_helper(temp_row, domain_size_arr):
	matrix_size = reduce(operator.mul, domain_size_arr, 1)
	curr_col = []
	# create and append columns to truth_value_matrix
	# ex. domain_size_arr = [4, 4]
	# example temp_row = []

	# for binary constraints
	# fill up last column, in pattern "a b c d", etc.
	if (len(domain_size_arr) == 1):
		for i in range(0, int(matrix_size / domain_size_arr[0])):
			for j in range(0, domain_size_arr[0]):
				curr_col.append(temp_row[j])

	if (len(domain_size_arr) > 1):
		for i in range(0, int(matrix_size / domain_size_arr[0])):
			for j in range(0, domain_size_arr[0]):
				curr_col.append(temp_row[j])

		for i in range(1, len(domain_size_arr)):
			for j in range(0, int(matrix_size / domain_size_arr[0])):
				for k in range(0, domain_size_arr[0]):
					curr_col.append(temp_row[j])

	# returns a filled in column for the truth matrix
	return curr_col

# generates the truth table string for n-ary constraints
def n_ary_constraints_string(truth_value_matrix, arr):
	return 0

# print(n_ary_constraints(['A_pet/dog', 'A_food=chocolate', '', '']))

#prints output to output.xml (writing)
with open('output.xml', 'a') as f:

	#prints header to xml file
	print("""<CSPIF VERSION="0.01">
	<CSP>
	<NAME>Untitled</NAME>
	<DESCRIPTION>
	<SHORT></SHORT>
	<DETAILED></DETAILED>
	</DESCRIPTION>\n""", file=f) 

	# prints to xml file the variables
	if (number_of_variables != 0):
		for i in range(1, number_of_variables + 1):
			print('\n'.join([convert_row_variables(data[i])]), file=f)

	# prints to xml file the alldiff constraints
	if (number_of_alldiff_constraints != 0):
		for i in range(number_of_variables + 2, number_of_variables + number_of_alldiff_constraints + 2):
			names = []
			for element in data[i]:
				if(element != ''):
					names.append(element)
			# print(names)
			combo = []
			for subset in combinations(names, 2):
				# print (subset)
				combo.append(subset)
			for j in range(0, len(combo)):
				print('\n'.join([convert_alldiff_constraints(combo[j], data[i])]), file=f)

	# prints to xml file the n-ary constraints
	if (number_of_nary_constraints != 0):
		for i in range(number_of_variables + number_of_alldiff_constraints + 3, number_of_variables + number_of_alldiff_constraints + number_of_nary_constraints + 3):
			print('\n'.join([n_ary(data[i])]), file=f)

	# testing on first n-ary constraint row
	# if (number_of_nary_constraints != 0):
	# 	print('\n'.join([n_ary(data[number_of_variables + number_of_alldiff_constraints + 3])]), file=f)	

	# prints footer to xml file
	print("""</CSP></CSPIF>""", file=f)

# instructions for user
print ('file is named "output.xml" in current directory')