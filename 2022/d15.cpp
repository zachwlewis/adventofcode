// adventofcode.com
// Day 15
// https://adventofcode.com/2022/day/15

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <cstdio>
#include <sstream>
#include <map>
#include <array>
#include <set>
#include <cmath>

#include "position.hpp"
#include "lines.hpp"

//#define SAMPLE

#ifdef SAMPLE
  #define INPUT_FILE "inputs/d15_sample.txt"
  #define TARGET_ROW 10
  #define EXTREMA 20
#else
  #define INPUT_FILE "inputs/d15.txt"
  #define TARGET_ROW 2000000
  #define EXTREMA 4000000
#endif // SAMPLE


struct SBPair
{
	SBPair(int x1, int y1, int x2, int y2) : sensor(Position(x1, y1)), beacon(Position(x2, y2))
	{
		manhattan = sensor.manhattan(beacon);
		left = sensor.x - manhattan;
		right = sensor.x + manhattan;
		top = sensor.y - manhattan;
		bottom = sensor.y + manhattan;

		// build perimeter set
		Position a = sensor + Position(manhattan + 1, 0);
		Position b = sensor + Position(0, manhattan + 1);
		Position c = sensor - Position(manhattan + 1, 0);
		Position d = sensor - Position(0, manhattan + 1);
		perimeter[0] = {a, b};
		perimeter[1] = {b, c};
		perimeter[2] = {c, d};
		perimeter[3] = {d, a};
	}

	Position sensor;
	Position beacon;
	int manhattan = 0;
	int top = 0;
	int left = 0;
	int bottom = 0;
	int right = 0;
	std::array<std::pair<Position, Position>, 4> perimeter;

	bool in_range(const Position& other) const { return other.manhattan(sensor) <= manhattan; }
};

Position find_empty(const std::vector<SBPair>& pairs)
{
	// For each sensor, find intersections with all other sensor ranges
	std::set<Position> intersections;
	const size_t num = pairs.size();
	for (size_t i = 0; i < num - 1; ++i)
	{
		const SBPair& a = pairs[i];

		for (size_t j = i + 1; j < num; ++j)
		{
			const SBPair& b = pairs[j];
			// Only check orthogonal pairs.
			Position ab_intersect;
			intersections.insert(intersection(a.perimeter[0].first, a.perimeter[0].second, b.perimeter[1].first, b.perimeter[1].second));
			intersections.insert(intersection(a.perimeter[0].first, a.perimeter[0].second, b.perimeter[3].first, b.perimeter[3].second));
			intersections.insert(intersection(a.perimeter[1].first, a.perimeter[1].second, b.perimeter[0].first, b.perimeter[0].second));
			intersections.insert(intersection(a.perimeter[1].first, a.perimeter[1].second, b.perimeter[2].first, b.perimeter[2].second));
			intersections.insert(intersection(a.perimeter[2].first, a.perimeter[2].second, b.perimeter[1].first, b.perimeter[1].second));
			intersections.insert(intersection(a.perimeter[2].first, a.perimeter[2].second, b.perimeter[3].first, b.perimeter[3].second));
			intersections.insert(intersection(a.perimeter[3].first, a.perimeter[3].second, b.perimeter[0].first, b.perimeter[0].second));
			intersections.insert(intersection(a.perimeter[3].first, a.perimeter[3].second, b.perimeter[2].first, b.perimeter[2].second));
		}
	}

	// We now have our set of intersections.
	// If the perimeter point is within another sensor, bail.
	// If it's not, we've found it!
	std::cout << "Found " << intersections.size() << " intersections across " << pairs.size() << " sensors." << std::endl;
	int i = 0;
	for (const Position& p : intersections) std::cout << ++i << "\t" << p << std::endl;


	for (const Position& p : intersections)
	{
		if (p.x < 0 || p.x > EXTREMA || p.y < 0 || p.y > EXTREMA)
			continue; // outside the search area. ignore it.
		std::cout << "Checking " << p << std::endl;
		bool found = false;
		for (const SBPair& sb : pairs)
		{
			if (sb.in_range(p))
			{
				found = true;
				break; // inside another sensors range.
			}
		}

		if (!found) return p;
	}
	
	return Position(INT_MIN,INT_MIN);
}

int main()
{
	std::ifstream input_file(INPUT_FILE);

	if (!input_file.is_open())
	{
		std::cout << "Unable to open input file: " << INPUT_FILE << std::endl;
		return 1;
	}

	size_t score1 = 0;
	size_t score2 = 0;
	std::vector<SBPair> pairs;
	Position min(INT_MAX), max(0);

	while (input_file.good())
	{
		std::string input_line;
		std::getline(input_file, input_line);
		if (input_line == "") break;

		std::stringstream ss(input_line);
		std::string x1buf, y1buf;
		std::string x2buf, y2buf;
		ss >> x1buf;
		ss >> y1buf;
		ss >> x2buf;
		ss >> y2buf;

		pairs.emplace_back(std::stoi(x1buf), std::stoi(y1buf), std::stoi(x2buf), std::stoi(y2buf));

		const SBPair& sb = pairs.back();

		if (sb.left < min.x) min.x = sb.left;
		if (sb.right > max.x) max.x = sb.right;
		if (sb.top < min.y) min.y = sb.top;
		if (sb.bottom > max.y) max.y = sb.bottom;
	}

	Position current(0,0);
	current.y = TARGET_ROW;
	for (int x = min.x; x < max.x; ++x)
	{
		current.x = x;
		for (const SBPair& sb : pairs)
		{
			if (sb.in_range(current))
			{
				++score1;
				if (current == sb.sensor || current == sb.beacon) --score1;
				break;
			}
		}
	}
	Position free = find_empty(pairs);
	std::cout << EXTREMA << std::endl;
	std::cout << "Found free space at " << free << std::endl;
	score2 = free.x * 4000000 + free.y;
	std::cout << "Part 1: " << score1 << std::endl;
	std::cout << "Part 2: " << score2 << std::endl;

	return 0;
}
