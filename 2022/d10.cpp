// adventofcode.com
// Day 10
// https://adventofcode.com/2022/day/10

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <cstdio>
#include <set>
#include <sstream>
#include <map>

#define INPUT_FILE "inputs/d10.txt"

const size_t MAX_COL = 39;
const size_t MAX_ROW = 5;

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
  std::string line = "", op = "";
  int val = 0;
  size_t clock = 0, ticks = 0;
  int x = 1;
	while (input_file.good())
	{
    if (ticks == 0)
    {
      std::getline(input_file, line);
      if (line == "") break; // EOF

      op = line.substr(0, 4);

      if (op == "noop") ticks = 1;
      if (op == "addx")
      {
        // handle add
        std::string value(line.begin()+5, line.end());
        val = std::stoi(value);
        ticks = 2;
      } 
    }

    

    // render
    int pos = clock % 40;
    if (pos >= x - 1 && pos <= x + 1) std::cout << "\u2588";
    else std::cout << " ";

    if (pos == MAX_COL) std::cout << std::endl;

    // tick clock
    ++clock;
    
    // update
    if ((clock + 20) % 40 == 0)
    {
      score1 += clock * x;
    }

    if (--ticks == 0)
    {
      // execute operation
      if (op == "addx") x += val;
      op = "";
      val = 0;
    }

    

	}
	
	std::cout << "Part 1: " << score1 << std::endl;
	// std::cout << "Part 2: " << score2 << std::endl;

	return 0;
}
