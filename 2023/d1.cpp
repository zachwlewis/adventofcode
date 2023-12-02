// adventofcode.com
// Day 1
// https://adventofcode.com/2023/day/1

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <algorithm>

#define INPUT_FILE "inputs/d1.txt"

int getCharDigitValue(char c) {
	int value = c - '0';
	if (value < 0 || value > 9) return -1;
	return value;
}

int main() {
	using namespace std;
	std::ifstream input_file (INPUT_FILE);
	std::string my_string;

	if (!input_file.is_open())
	{
		std::cout << "Unable to open input file: " << INPUT_FILE << std::endl;
		return 1;
	}

	int answer1 = 0;
	int line = 1;

	while (input_file)
	{
		std::string str;
		std::getline(input_file, str);
		if (str.empty()) break;
		
		// find the first and last character where getCharDigitValue is not -1
		std::string::iterator start = str.begin();
		std::string::iterator end = str.end() - 1;

		while (start <= end) {
			if (getCharDigitValue(*start) != -1) {
				break;
			}
			++start;
		}

		while (end >= start) {
			if (getCharDigitValue(*end) != -1) {
				
				break;
			}
			--end;
		}

		int first = getCharDigitValue(*start);
		int last = getCharDigitValue(*end);
		int total = 10 * first + last;

		answer1 += total;
	}

	std::cout << "Answer 1: " << answer1 << std::endl;

	std::ifstream input_file2 (INPUT_FILE);

	int answer2 = 0;
	while (input_file2) {
		std::string str;
		std::getline(input_file2, str);
		if (str.empty()) break;
		
		std::vector<std::string> names = {"one", "two", "three", "four", "five", "six", "seven", "eight", "nine"};
		std::vector<std::string> digits = {"1", "2", "3", "4", "5", "6", "7", "8", "9"};
		
		int first = 0;
		int firstidx = 100000;
		int last = 0;
		int lastidx = -1;

		for (int i = 0; i < 9; ++i)
		{
			// Find the first position of the digit
			int first_position = str.find(names[i]);
			int first_value = str.find(digits[i]);
			
			if (first_position == -1) {
				first_position = first_value;
			} else if (first_value != -1 && first_value < first_position) {
				first_position = first_value;
			}

			if (first_position != -1 && first_position < firstidx)
			{
				// This is the firstest number so far.
				firstidx = first_position;
				first = i + 1;
			}

			int last_position = str.rfind(names[i]);
			int last_value = str.rfind(digits[i]);

			if (last_position == -1) {
				last_position = last_value;
			} else if (last_value != -1 && last_value > last_position) {
				last_position = last_value;
			}

			if (last_position != -1 && last_position > lastidx) {
				// This is the lastest number so far
				lastidx = last_position;
				last = i + 1;
			}
		}

		int total = 10 * first + last;
		
		answer2 += total;

	}

	std::cout << "Answer 2: " << answer2 << std::endl;

	return 0;
}