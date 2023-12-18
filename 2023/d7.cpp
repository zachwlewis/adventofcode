// adventofcode.com
// Day 7: Camel Cards
// https://adventofcode.com/2023/day/7

#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <map>
#include <algorithm>
#include <format>
#include "stringtools.hpp"
#include "range.hpp"

#define INPUT_FILE "inputs/d7.txt"

uint getRank(const std::vector<char>& cards) {
	// 0: high card
	// 1: pair
	// 2: two pair
	// 3: three of a kind
	// 4: full house
	// 5: four of a kind
	// 6: five of a kind

	std::map<char, uint> card_count;
	for (auto& card : cards) {
		card_count[card]++;
	}

	std::map<uint, uint> count_count;
	for (auto& [card, count] : card_count) {
		count_count[count]++;
	}

	uint rank = 0;
	if (count_count[5] == 1) {
		rank = 6;
	} else if (count_count[4] == 1) {
		rank = 5;
	} else if (count_count[3] == 1 && count_count[2] == 1) {
		rank = 4;
	} else if (count_count[3] == 1) {
		rank = 3;
	} else if (count_count[2] == 2) {
		rank = 2;
	} else if (count_count[2] == 1) {
		rank = 1;
	}

	return rank;
}

uint getCardValue(char card) {
	if (card == 'A') {
		return 14;
	} else if (card == 'K') {
		return 13;
	} else if (card == 'Q') {
		return 12;
	} else if (card == 'J') {
		return 11;
	} else if (card == 'T') {
		return 10;
	} else {
		return card - '0';
	}
}

struct Hand {

	Hand(std::string s) {
		auto parts = split(s, ' ');
		bet = std::stoi(parts[1]);
		for (auto& card : parts[0]) {
			cards.push_back(card);
			values.push_back(getCardValue(card));
		}

		rank = getRank(cards);
	}

	uint bet = 0;
	std::vector<char> cards;
	std::vector<uint> values;
	uint rank = 0;

	bool operator<(const Hand& other) const {
		if (rank != other.rank) {
			return rank < other.rank;
		}

		for (uint i = 0; i < 5; ++i) {
			uint v1 = values[i];
			uint v2 = other.values[i];
			if (v1 != v2) {
				return v1 < v2;
			}
		}

		return false;
	}

	bool operator==(const Hand& other) const {
		if (rank != other.rank) {
			return false;
		}

		for (uint i = 0; i < 5; ++i) {
			uint v1 = values[i];
			uint v2 = other.values[i];
			if (v1 != v2) {
				return false;
			}
		}

		return true;
	}

	bool operator>(const Hand& other) const {
		return !(*this < other) && !(*this == other);
	}
};

inline std::ostream & operator<<(std::ostream & Str, Hand const & v) { 
	Str << "[" << v.rank << "] ";
	for (auto& card : v.cards) {
		Str << card;
	}
	Str << " " << v.bet;
	return Str;
}

int main() {

	std::ifstream input_file (INPUT_FILE);

	if (!input_file.is_open())
	{
		std::cout << "Unable to open input file: " << INPUT_FILE << std::endl;
		return 1;
	}

	uint64_t answer1 = 0;
	uint64_t answer2 = 0;
	std::string line;
	std::vector<Hand> hands;

	while(std::getline(input_file, line)) {
		if (line.empty()) {
			continue;
		}

		Hand hand(line);
		hands.push_back(hand);
		std::cout << hand << std::endl;
	}

	// Sort hands with the lowest first
	std::sort(hands.begin(), hands.end());

	std::cout << std::endl;

	uint rank = 1;
	for (auto& hand : hands) {
		std::cout << hand << std::endl;
		std::cout << rank << " * " << hand.bet << std::endl;
		answer1 += rank * hand.bet;
		rank++;
	}

	std::cout << "Answer 1: " << answer1 << std::endl;
	std::cout << "Answer 2: " << answer2 << std::endl;

	return 0;
}