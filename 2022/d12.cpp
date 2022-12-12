// adventofcode.com
// Day 12
// https://adventofcode.com/2022/day/12

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <cstdio>
#include <set>
#include <sstream>
#include "position.hpp"

#define INPUT_FILE "inputs/d12.txt"

const Position UP    = { 0, -1};
const Position LEFT  = {-1,  0};
const Position DOWN  = { 0,  1};
const Position RIGHT = { 1,  0};

void start_to_end(Position p, Position t, int step, const std::vector<std::vector<int>> &heightmap, std::vector<std::vector<size_t>> &stepmap)
{
  // solve the map recursively, prioritizing higher numbers
  if (step >= stepmap[p.y][p.x])
    return; // there's already a shorter path

  stepmap[p.y][p.x] = step; // memoize the shortest number of steps to reach each position
  
  if (p == t)
  {
    //std::cout << "Path found: " << p.tostring() << " " << step << std::endl;
    return; // we're at the end!
  }

  
  const size_t X_MAX = heightmap[0].size() - 1;
  const size_t Y_MAX = heightmap.size() - 1;
  std::vector<Position> next_steps = {
    p + UP,
    p + LEFT,
    p + DOWN,
    p + RIGHT,
  };

  for (Position np : next_steps)
  {
    if (np.x < 0 || np.x > X_MAX || np.y < 0 || np.y > Y_MAX)
      continue; // out of bounds
    
    int height = heightmap[np.y][np.x];
    if (height > heightmap[p.y][p.x] + 1)
      continue; // position is too high!

    // we can take this step.
    start_to_end(np, t, step + 1, heightmap, stepmap);
  }
}

void end_to_a(Position p, int step, const std::vector<std::vector<int>> &heightmap, std::vector<std::vector<size_t>> &stepmap)
{
  // solve the map recursively, prioritizing higher numbers
  if (step >= stepmap[p.y][p.x])
    return; // there's already a shorter path

  stepmap[p.y][p.x] = step; // memoize the shortest number of steps to reach each position
  
  if (heightmap[p.y][p.x] == 0)
  {
    //std::cout << "Path found: " << p.tostring() << " " << step << std::endl;
    return; // we're at the end!
  }

  
  const size_t X_MAX = heightmap[0].size() - 1;
  const size_t Y_MAX = heightmap.size() - 1;
  std::vector<Position> next_steps = {
    p + UP,
    p + LEFT,
    p + DOWN,
    p + RIGHT,
  };

  for (Position np : next_steps)
  {
    if (np.x < 0 || np.x > X_MAX || np.y < 0 || np.y > Y_MAX)
      continue; // out of bounds
    
    int height = heightmap[np.y][np.x];
    if (heightmap[p.y][p.x] > height + 1)
      continue; // position is too high!

    // we can take this step.
    end_to_a(np, step + 1, heightmap, stepmap);
  }
}


int main() {

	std::ifstream input_file(INPUT_FILE);

	if (!input_file.is_open())
	{
		std::cout << "Unable to open input file: " << INPUT_FILE << std::endl;
		return 1;
	}

	size_t score1 = 0;
	size_t score2 = SIZE_MAX;
  Position step; // iterator position
  Position start; // start location
  Position target; // target location
  std::vector<std::vector<int>> heightmap = {};
  std::vector<std::vector<size_t>> stepmap = {};
  std::vector<std::vector<size_t>> pathmap = {};
  std::vector<Position> paths = {};
  // populate map
	while (input_file.good())
	{
    std::string line;
    std::getline(input_file, line);
    if (line == "") break;
    heightmap.push_back({});
    stepmap.push_back({});
    pathmap.push_back({});
    step.x = 0;
    for (char c : line)
    {
      if (c == 'S')
      {
        c = 'a';
        start = step;
      }

      if (c == 'a')
        paths.push_back(step); // potential hiking spot!

      if (c == 'E')
      {
        c = 'z';
        target = step;
      }
      ++step.x;

      heightmap[step.y].push_back(c - 'a');
      stepmap[step.y].push_back(INT_MAX);
      pathmap[step.y].push_back(INT_MAX);
    }

    ++step.y;
	}

  std::cout << start.tostring() << " " << target.tostring() << std::endl;
  start_to_end(start, target, 0, heightmap, stepmap);
  score1 = stepmap[target.y][target.x];

  end_to_a(target, 0, heightmap, pathmap);

  for (Position p : paths)
  {
    if (pathmap[p.y][p.x] < score2)
      score2 = pathmap[p.y][p.x];
  }
 	
	std::cout << "Part 1: " << score1 << std::endl;
	std::cout << "Part 2: " << score2 << std::endl;

	return 0;
}
