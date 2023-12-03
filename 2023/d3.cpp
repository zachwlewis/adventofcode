// adventofcode.com
// Day 3
// https://adventofcode.com/2023/day/3

#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <map>
#include <algorithm>
#include "position.hpp"

#define INPUT_FILE "inputs/d3.txt"

/** The type of character. */
enum class CharType : uint8_t {
	NONE,
	DIGIT,
	SYMBOL,
};

CharType GetCharType(const char& c) {
	if (c >= '0' && c <= '9') return CharType::DIGIT;
	if (c == '.') return CharType::NONE;
	return CharType::SYMBOL;
};

struct SchematicNumber {
	Position start;
	std::string number_string;
	Position top_left() const { return start + Position(-1, -1); }
	Position bottom_right() const { return start + Position(number_string.length(), 1); }
	int value() const { return std::stoi(number_string); }
};

struct SchematicSymbol {
	Position position;
	char symbol;
	std::vector<SchematicNumber> adjacent_numbers;
	bool isGear() const { return symbol == '*'; }
};

inline std::ostream & operator<<(std::ostream & Str, SchematicNumber const & v) { 
  Str << v.start << ": " << v.number_string << " (" << v.top_left() << " - " << v.bottom_right() << ")";
  return Str;
}

inline std::ostream & operator<<(std::ostream & Str, SchematicSymbol const & v) { 
  Str << v.position << ": " << v.symbol << " <| ";
  for (auto& number : v.adjacent_numbers) {
	  Str << " " << number.value();
  }
  return Str;
}

std::vector<SchematicSymbol*> findAdjacentSymbols(const SchematicNumber& schematic_number, std::map<Position, SchematicSymbol>& schematic_symbols) {
	std::vector<SchematicSymbol*> symbols;
	for (int x = schematic_number.top_left().x; x <= schematic_number.bottom_right().x; ++x) {
		for (int y = schematic_number.top_left().y; y <= schematic_number.bottom_right().y; ++y) {
			Position position(x, y);
			if (schematic_symbols.find(position) != schematic_symbols.end()) {
				symbols.push_back(&schematic_symbols[position]);
			}
		}
	}

	return symbols;
}

int main() {

	std::ifstream input_file (INPUT_FILE);
	std::string my_string;

	if (!input_file.is_open())
	{
		std::cout << "Unable to open input file: " << INPUT_FILE << std::endl;
		return 1;
	}

	int answer1 = 0;
	int answer2 = 0;
	int line = 0;

	std::vector<SchematicNumber> schematic_numbers;
	std::map<Position, SchematicSymbol> schematic_symbols;

	while (input_file)
	{
		std::string str;
		std::getline(input_file, str);
		if (str.empty()) break;

		size_t length = str.length();
		std::string::iterator start = str.begin();
		std::string::iterator end = str.end() - 1;
		
		bool in_number = false;
		size_t number_start = 0;
		
		for (size_t i = 0; i < length; ++i) {
			CharType type = GetCharType(str[i]);
			
			if (type == CharType::DIGIT) {
				number_start = i;
				size_t number_size = 1;
				while (i + number_size < length && GetCharType(str[i + number_size]) == CharType::DIGIT) {
					++number_size;
				}
				std::string number_str = str.substr(number_start, number_size);
				schematic_numbers.push_back({{static_cast<int>(i), static_cast<int>(line)}, number_str});
				i += number_size -1;
			} else if (type == CharType::SYMBOL) {
				Position position(i, line);
				schematic_symbols[position] = {position, str[i]};
			}
		}

		++line;
	}

	// Find each adjacent symbol and register this number with the symbol.
	for (auto& schematic_number : schematic_numbers) {
		auto adjacentSymbols = findAdjacentSymbols(schematic_number, schematic_symbols);
		if (adjacentSymbols.size() != 0) {
			answer1 += schematic_number.value();
		}

		for (auto& adjacentSymbol : adjacentSymbols) {
			adjacentSymbol->adjacent_numbers.push_back(schematic_number);
		}
	}

	for (auto& [position, symbol] : schematic_symbols) {
		if (symbol.isGear() && symbol.adjacent_numbers.size() == 2) {
			answer2 += symbol.adjacent_numbers[0].value() * symbol.adjacent_numbers[1].value();
		}
	}

	std::cout << "Answer 1: " << answer1 << std::endl;
	std::cout << "Answer 2: " << answer2 << std::endl;

	

	return 0;
}