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

#include "position.hpp"


#define INPUT_FILE "inputs/d14.txt"

enum class Material : int
{
  Air = 0,
  Rock = 1,
  Sand = 2,
};

using SandMap = std::map<Position, Material>;

/* The possible movements of falling sand. */
const std::array<Position, 3> SAND_MOVES = {Position(0,1), Position(-1,1), Position(1,1)};

/* Moves sand down in the map.
 * @return Is the sand at rest?
 */
bool sand_step(Position &ioSand, const SandMap &inMap)
{
  for (const Position& move : SAND_MOVES)
  {
    Position p = ioSand + move;
    if (!inMap.contains(p) || inMap.at(p) == Material::Air)
    {
      ioSand += move;
      return false;
    }
  }

  return true;
}

void print_map(Position min, Position max, const SandMap& map, const std::set<Position>& path)
{
  min -= Position(1,1);
  max += Position(1,1);
  Position i(min);
  std::cout << min << std::endl;
  while (i != max)
  {

    Material m = map.contains(i) ? map.at(i) : Material::Air;
    char out = m == Material::Air ? '.' : m == Material::Rock ? '#' : 'o';
    bool on_path = path.contains(i);
    if (on_path) std::cout << "\033[1;35m";
    std::cout << out;
    if (on_path) std::cout << "\033[0m";

    i.x++;

    if (i.x > max.x)
    {
      // new row
      i.x = min.x;
      i.y++;
      std::cout << std::endl;
    }
  }
  std::cout << max << std::endl;
}

int main() {

	std::ifstream input_file(INPUT_FILE);

	if (!input_file.is_open())
	{
		std::cout << "Unable to open input file: " << INPUT_FILE << std::endl;
		return 1;
	}
  
  SandMap sandmap;

	size_t score1 = 0;
	size_t score2 = 0;

  Position top_left = {INT_MAX, 0};
  Position bottom_right = {0,0};
  const Position SAND_HOLE(500, 0);

  // build our map
	while (input_file.good())
	{
    std::string input_line;
    std::getline(input_file, input_line);
    if (input_line == "") break;

    std::stringstream ss(input_line);
    std::string xbuf, ybuf;
    std::vector<Position> vertices;

    while (ss >> xbuf && ss >> ybuf)
    {
      int x = std::stoi(xbuf);
      int y = std::stoi(ybuf);
      if (top_left.x > x) top_left.x = x;
      if (top_left.y > y) top_left.y = y;
      if (bottom_right.x < x) bottom_right.x = x;
      if (bottom_right.y < y) bottom_right.y = y;
      vertices.emplace_back(x, y);
    }

    for (size_t i = 1; i < vertices.size(); ++i)
    {
      const Position& from = vertices[i-1];
      const Position& to = vertices[i];
      Position current(from);
      Position step = (to - from).normalize();
      while (current != to + step)
      {
        sandmap[current] = Material::Rock;
        current += step;
      }
    }
	}

  SandMap map1(sandmap);
  // start pumping out sand
  Position sand(SAND_HOLE);
  std::set<Position> path;
  while (sand.y < bottom_right.y)
  {
    if (sand_step(sand, map1))
    {
      // the sand has come to rest.
      ++score1; 
      // update the map and spawn more sand.
      map1[sand] = Material::Sand;
      sand = Position(SAND_HOLE);
      path.clear();
    }
    path.insert(sand);
  }

  print_map(top_left, bottom_right, map1, path);

  // part 2
  sand = Position(SAND_HOLE);
  while (true)
  {
    bool at_rest = sand_step(sand, sandmap);
    if (at_rest || sand.y == bottom_right.y + 1)
    {
      // the sand has come to rest.
      ++score2; 
      // update the map and spawn more sand.
      sandmap[sand] = Material::Sand;
      if (sand == SAND_HOLE)
      {
        // we're all full!
        break;
      }
      sand = Position(SAND_HOLE);
      path.clear();
    }
    path.insert(sand);
  }

  print_map(top_left, bottom_right, sandmap, path);

	std::cout << "Part 1: " << score1 << std::endl;
	std::cout << "Part 2: " << score2 << std::endl;

	return 0;
}
