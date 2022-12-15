// adventofcode.com
// Day 14
// https://adventofcode.com/2022/day/14

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

// #define SAMPLE
// #define ONE_SET
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
    std::cout << "Constructing SBPair" << std::endl;
    bounds(l, t, r, b);
    Position p(l, t);
    for (int y = t; y <= b; ++y)
    {
      p.y = y;
      for (int x = l; x <= r; ++x)
      {
        p.x = x;
        int m = p.manhattan(sensor);
        if (m <= manhattan())
          cset.insert(p);
      }
    }
  }
  Position sensor;
  Position beacon;
  std::set<Position> cset;
  int t, l, b, r;
  int manhattan() const { return sensor.manhattan(beacon); }
  bool in_range(const Position& other) const
  {
    // int m = other.manhattan(sensor);
    // return m <= manhattan();
    return cset.contains(other);
  }

  void bounds(int& left, int& top, int& right, int& bottom) const
  {
    int m = manhattan();
    left = sensor.x - m;
    right = sensor.x + m;
    top = sensor.y - m;
    bottom = sensor.y + m;
  }
};

Position find_empty(const std::vector<SBPair>& pairs)
{
  std::cout << "find_empty()" << std::endl;
  std::set<Position> search;
  Position current(0,0);
#ifdef ONE_SET
  for (const SBPair& sb : pairs)
  {
    for (const Position& p : sb.cset)
      search.insert(p);
  }
#endif // ONE_SET
  for (int y = 0; y <= EXTREMA ; ++y)
  {
    std::cout << "Row: " << y << "                            \r";
    current.y = y;
    for (int x = 0; x <= EXTREMA ; ++x)
    {
      current.x = x;
    std::cout << "Row: " << current << "                            \r";

      bool found = false;
      
      // reduce our search set
#ifndef ONE_SET
      search.clear();
      for (const SBPair& sb : pairs)
      {
        int top, left, bottom, right;
        sb.bounds(left, top, right, bottom);
        if (x < left ||  x > right || y < top || y > bottom)
          continue;
        
        for (const Position& p : sb.cset)
          search.insert(p);
      }
#endif

      if (!search.contains(current)) return current;

      // for (const SBPair* sb : search)
      // {
      //   if (sb->in_range(current))
      //   {
      //     found = true;
      //     // Position delta = sb.sensor - current;
      //     // int offset = (sb.beacon - sb.sensor).size().x - delta.size().x;
      //     // x += (delta.size().x + offset) * 2 + 1;
      //     break;
      //   }
      // }
      //if (!found) return current;
    }
  }
  return current;
}

int main() {

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

    int left, right, top, bottom;
    pairs.back().bounds(left, top, right, bottom);

    if (left < min.x) min.x = left;
    if (right > max.x) max.x = right;
    if (top < min.y) min.y = top;
    if (bottom > max.y) max.y = bottom;
	}
  std::cout << "processing done" << std::endl;
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
  std::cout << "p1 done" << std::endl;

  Position free = find_empty(pairs);

  std::cout << free << std::endl;

  

  std::cout << std::endl;
  std::cout << free << std::endl;
  
  score2 = free.x * 4000000 + free.y;
	std::cout << "Part 1: " << score1 << std::endl;
	std::cout << "Part 2: " << score2 << std::endl;

	return 0;
}
