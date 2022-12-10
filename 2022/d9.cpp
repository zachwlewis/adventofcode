// adventofcode.com
// Day 9
// https://adventofcode.com/2022/day/9

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <cstdio>
#include <set>
#include <sstream>
#include <map>

#define INPUT_FILE "inputs/d9.txt"

struct Position
{
  int x = 0;
  int y = 0;
  Position& operator+=(const Position& rhs)
  {
    x += rhs.x;
    y += rhs.y;
    return *this;
  }
  Position& operator -=(const Position& rhs)
  {
    x -= rhs.x;
    y -= rhs.y;
    return *this;
  }
  friend Position operator+(Position lhs, const Position& rhs)
  {
    lhs += rhs;
    return lhs;
  }
  friend Position operator-(Position lhs, const Position& rhs)
  {
    lhs -= rhs;
    return lhs;
  }
  friend bool operator<(const Position& l, const Position& r) { return l.x < r.x || (l.x==r.x && l.y < r.y); }
  friend bool operator>(const Position& l, const Position& r) { return r.x < l.x; }
  friend bool operator<=(const Position& l, const Position& r) { return !(l.x > r.x); }
  friend bool operator>=(const Position& l, const Position& r) { return !(l.x < r.x); }
  Position normalize() const
  {
    Position out;
    out.x = x == 0 ? 0 : x / std::abs(x);
    out.y = y == 0 ? 0 : y / std::abs(y);
    return out;
  }
  Position size() const { return {std::abs(x), std::abs(y)}; }
  std::string tostring() const
  {
    std::stringstream ss;
    ss << "{" << x << ", " << y << "}";
    return ss.str();
  }
};

Position parse_char(char c)
{
  if (c == 'L') return {-1,  0};
  if (c == 'R') return { 1,  0};
  if (c == 'U') return { 0,  1};
  if (c == 'D') return { 0, -1};
  std::cout << "bad char: " << c << std::endl;
  return {0, 0};
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

  char direction, blank;
  std::string s_steps;
  
  Position rope[10];
  std::set<Position> first_knot_locations = {};
  std::set<Position> last_knot_locations = {};
  //std::cout << "Head: " << head.tostring() << std::endl;
  //std::cout << "Tail: " << tail.tostring() << std::endl;
	while (input_file.good())
	{
		input_file.get(direction);
		input_file.get(blank);
    Position move = parse_char(direction);
    std::getline(input_file, s_steps);
    size_t steps = std::stoi(s_steps);
    if (s_steps == "") break;
    //std::cout << direction << blank << s_steps << std::endl;

    // std::cout << "---------" << std::endl;
    // std::cout << "Move: " << direction << " " << move.tostring() << " x" << steps << std::endl;

    for (size_t step = 0; step < steps; ++step)
    {
      // Move the head.
      rope[0] += move;
      for (size_t knot = 1; knot < 10; ++knot)
      {
        Position delta = rope[knot - 1] - rope[knot];
        Position delta_size = delta.size();
        if (delta_size.x > 1 || delta_size.y > 1)
          rope[knot] += delta.normalize();
      }
      first_knot_locations.insert(rope[1]);
      last_knot_locations.insert(rope[9]);
      // Check if the tail needs to move
      // std::cout << "---------" << std::endl;
      // std::cout << "Head: " << head.tostring() << std::endl;
      // std::cout << "Tail: " << tail.tostring() << std::endl;
      // std::cout << "D: " << delta.tostring() << "DS: " << delta_size.tostring() << "N: " << delta.normalize().tostring() << std::endl;
      

      // std::cout << "Tail End: " << tail.tostring() << std::endl;
    }

	}

  score1 = first_knot_locations.size();
  score2 = last_knot_locations.size();
	std::cout << "Part 1: " << score1 << std::endl;
	std::cout << "Part 2: " << score2 << std::endl;

	return 0;
}
