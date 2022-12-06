// adventofcode.com
// Day 6
// https://adventofcode.com/2022/day/6

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <cstdio>
#include <set>
#include <sstream>

#define INPUT_FILE "inputs/d6.txt"

void print_buffer(const std::vector<char> &inBuffer){
  std::cout << "B: ";
  for (auto i = inBuffer.begin(); i < inBuffer.end(); ++i)
  {
    std::cout << *i;
  }
  std::cout << "(" << inBuffer.size() << ")" << std::endl;
}

int main() {

  std::ifstream input_file (INPUT_FILE);

  if (!input_file.is_open())
  {
    std::cout << "Unable to open input file: " << INPUT_FILE << std::endl;
    return 1;
  }

  int score1 = 0;
  int score2 = 0;
  std::vector<char> buffer = {};

  char input = '-';
  while (input_file.good())
  {
    input_file.get(input);
    ++score1;
    //std::printf("[%d] %c => ", score1, input);
    //print_buffer(buffer);

    for (size_t i = 0; i < buffer.size(); ++i)
    {
      if (input == buffer[i])
      {
        //std::cout << input << " = " << buffer[i] << " @ " << i << std::endl;
        buffer.erase(buffer.begin(), buffer.begin() + i + 1);
        break;
      }
    }

    buffer.push_back(input);
    if (buffer.size() == 4) break;
  }

  print_buffer(buffer);
  std::cout << "Part 1: " << score1 << std::endl;

  input_file.seekg(0);
  buffer.clear();
  while (input_file.good())
  {

    input_file.get(input);
    ++score2;
    //std::printf("[%d] %c => ", score2, input);
    //print_buffer(buffer);

    for (size_t i = 0; i < buffer.size(); ++i)
    {
      if (input == buffer[i])
      {
        //std::cout << input << " = " << buffer[i] << " @ " << i << std::endl;
        buffer.erase(buffer.begin(), buffer.begin() + i + 1);
        break;
      }
    }

    buffer.push_back(input);
    if (buffer.size() == 14) break;
  }
  
  print_buffer(buffer);
  std::cout << "Part 2: " << score2 << std::endl;

  return 0;
}
