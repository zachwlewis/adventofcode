// adventofcode.com
// Day 4
// https://adventofcode.com/2022/day/4

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <cstdio>
#include <set>
#include <sstream>

#define INPUT_FILE "inputs/d4.txt"

/** Defines an integer range. */
struct Range
{
  int min = 0;
  int max = 0;

  Range(int inMin, int inMax)
  : min(inMin), max(inMax) {}

  /** Does this Range fully include another Range? */
  bool includes(const Range &inRange) const
  {
    if (min > inRange.min) return false;
    if (max < inRange.max) return false;
    return true;
  }

  /** Does this Range overlap another Range? */
  bool overlaps(const Range &inRange) const
  {
    int overlap_start = std::max<int>(min, inRange.min);
    int overlap_end = std::min<int>(max, inRange.max);
    if (overlap_start > overlap_end) return false;
    return true;
  }
};

int main() {

  std::ifstream input_file (INPUT_FILE);
  std::string my_string;

  if (!input_file.is_open())
  {
    std::cout << "Unable to open input file: " << INPUT_FILE << std::endl;
    return 1;
  }

  size_t line_count = 0;
  int score1 = 0;
  int score2 = 0;
  while (input_file)
  {
    std::string line;
    std::getline(input_file, line);

    if (line.length() == 0)
      break;

    std::string minA = "", maxA = "", minB = "", maxB = "";
    std::stringstream s_stream(line);
    std::getline(s_stream, minA, '-');
    std::getline(s_stream, maxA, ',');
    std::getline(s_stream, minB, '-');
    std::getline(s_stream, maxB);

    Range a(std::stoi(minA), std::stoi(maxA));
    Range b(std::stoi(minB), std::stoi(maxB));
    bool fully_includes = a.includes(b) || b.includes(a);
    bool has_overlap = a.overlaps(b);

    if (fully_includes) ++score1;
    if (has_overlap) ++score2;
    
    ++line_count;
  }

  std::cout << "Lines: " << line_count << std::endl;
  std::cout << "Part 1: " << score1 << std::endl;
  std::cout << "Part 2: " << score2 << std::endl;
  return 0;
}
