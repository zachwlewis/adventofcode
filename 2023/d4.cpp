// adventofcode.com
// Day 4: Scoring Lottery Tickets
// https://adventofcode.com/2023/day/4

#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <map>
#include <algorithm>
#include "stringtools.hpp"

#define INPUT_FILE "inputs/d4.txt"

struct Ticket {
	int id;
	std::vector<int> winning_numbers;
	std::vector<int> ticket_numbers;
	int copies = 1;
	int matches() const {
		int score = 0;
		auto start = winning_numbers.begin();
		auto end = winning_numbers.end();
		for (auto& number : ticket_numbers) {
			if (std::find(start, end, number) != end) {
				score++;
			}
		}
		return score;
	}
};

inline std::ostream & operator<<(std::ostream & Str, Ticket const & v) { 
  Str << "[" << v.copies << "] Ticket " << v.id + 1 << ": ";
  for (auto& number : v.winning_numbers) {
	  Str << number << " ";
  }

  Str << " | ";

  for (auto& number : v.ticket_numbers) {
	  Str << number << " ";
  }

  return Str;
}

int score_ticket(const Ticket& ticket) {
	int score = 0;

	auto start = ticket.winning_numbers.begin();
	auto end = ticket.winning_numbers.end();
	for (auto& number : ticket.ticket_numbers) {
		if (std::find(start, end, number) != end) {
			score++;
		}
	}

	 return score > 0 ? std::pow(2, score - 1) : 0;
}

int main() {

	std::ifstream input_file (INPUT_FILE);

	if (!input_file.is_open())
	{
		std::cout << "Unable to open input file: " << INPUT_FILE << std::endl;
		return 1;
	}

	int answer1 = 0;
	int answer2 = 0;
	int line = 0;

	std::vector<Ticket> tickets;

	while (input_file)
	{
		std::string str;
		std::getline(input_file, str);
		if (str.empty()) break;

		std::vector<std::string> ticket = split(str, ':');
		std::vector<std::string> numbers = split(ticket[1], '|');
		std::vector<std::string> winning_number_string = split(numbers[0], ' ');
		std::vector<std::string> ticket_number_string = split(numbers[1], ' ');

		std::vector<int> winning_numbers;
		for (auto& number : winning_number_string) {
			if (!number.empty()) {
				winning_numbers.push_back(std::stoi(number));
			}
		}
		
		std::vector<int> ticket_numbers;
		for (auto& number : ticket_number_string) {
			if (!number.empty()) {
				ticket_numbers.push_back(std::stoi(number));
			}
		}

		tickets.push_back({line++, winning_numbers, ticket_numbers});
	}

	for (int i = 0; i < tickets.size(); i++) {
		answer1 += score_ticket(tickets[i]);
	}

	// Iterate backwards over the tickets to memoize the score.
	for (int i = tickets.size() - 1; i >= 0; --i) {
		int matches = tickets[i].matches();
		for (int j = 0; j < matches; ++j)
		{
			tickets[i].copies += tickets[i + j + 1].copies;
		}

		answer2 += tickets[i].copies;
	}

	std::cout << "Answer 1: " << answer1 << std::endl;
	std::cout << "Answer 2: " << answer2 << std::endl;

	return 0;
}