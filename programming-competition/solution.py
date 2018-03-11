#!/usr/bin/env python
import sys

def read_salary(line):
	value = line.split(",")[1]
	return value

def correct_position(line, position):
	value = line.split(",")[2]
	if value in position:
		return 1
	return 0

def find_max(position):	
	with open(sys.argv[1]) as f:
		max_points = 0	
		max_line = ""
		for line in f:
			if (read_salary(line) > max_points) and (correct_position(line, position)):
				max_points = read_salary(line)
				max_line = line
		return max_line

def main():
	max_size = 10
	positions = ['center', 'forward', 'shooting guard', 'point guard']
	player_lineup = []

	for position in positions:
		player_lineup.append(find_max(position))

	for player in player_lineup:	
		print(player)

if __name__ == "__main__":
	main()