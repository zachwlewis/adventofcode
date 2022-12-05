// adventofcode.com
// Day 5
// https://adventofcode.com/2022/day/5

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <cstdio>
#include <set>
#include <sstream>

#define INPUT_FILE "inputs/d5.txt"


int main() {

  std::vector<std::vector<char>> stack = {
    {'G','D','V','Z','J','S','B'},
    {'Z','S','M','G','V','P'},
    {'C','L','B','S','W','T','Q','F'},
    {'H','J','G','W','M','R','V','Q'},
    {'C','L','S','N','F','M','D'},
    {'R','G','C','D'},
    {'H','G','T','R','J','D','S','Q'},
    {'P','F','V'},
    {'D','R','S','T','J'},
  };

  std::vector<std::vector<char>> stack2 = {
    {'G','D','V','Z','J','S','B'},
    {'Z','S','M','G','V','P'},
    {'C','L','B','S','W','T','Q','F'},
    {'H','J','G','W','M','R','V','Q'},
    {'C','L','S','N','F','M','D'},
    {'R','G','C','D'},
    {'H','G','T','R','J','D','S','Q'},
    {'P','F','V'},
    {'D','R','S','T','J'},
  };

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

    std::string s_repeat = "", s_from = "", s_to = "";
    std::stringstream s_stream(line);
    std::getline(s_stream, s_repeat, ',');
    std::getline(s_stream, s_from, ',');
    std::getline(s_stream, s_to);

    int repeat = std::stoi(s_repeat);
    int from = std::stoi(s_from) - 1;
    int to = std::stoi(s_to) - 1;

    for (size_t i = 0; i < repeat; ++i)
    {
      stack[to].push_back(stack[from].back());
      stack[from].pop_back();
    }

    std::vector<char> claw = {};
    // Load the claw
    for (size_t i = 0; i < repeat; ++i)
    {
      claw.push_back(stack2[from].back());
      stack2[from].pop_back();
    }

    // Empty the claw
    for (size_t i = 0; i < repeat; ++i)
    {
      stack2[to].push_back(claw.back());
      claw.pop_back();
    }
    
    ++line_count;
  }

  std::cout << "Lines: " << line_count << std::endl;
  std::cout << "Part 1: ";
  for (size_t i = 0; i < stack.size(); ++i)
  {
    std::cout << stack[i].back();
  }
  std::cout << std::endl;
  std::cout << "Part 2: ";
  for (size_t i = 0; i < stack.size(); ++i)
  {
    std::cout << stack2[i].back();
  }
  std::cout << std::endl;
  return 0;
}
