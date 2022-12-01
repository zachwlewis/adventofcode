// adventofcode.com
// Day 1
// https://adventofcode.com/2022/day/1

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>

int main() {
    std::ifstream input_file ("inputs/d1.txt");
    std::string my_string;

    if (!input_file.is_open())
    {
      std::cout << "Unable to open input!" << std::endl;
      return 1;
    }

    int calories = 0;
    std::vector<int> calories_list;
    while (input_file)
    {
      std::string line;
      std::getline(input_file, line);
      if (line.length() == 0)
      {
        calories_list.push_back(calories);
        calories = 0;
        continue;
      }

      calories += std::stoi(line);
    }

    std::sort(calories_list.begin(), calories_list.end(), std::greater<int>());
    std::cout << calories_list[0] << std::endl;
    std::cout << calories_list[0] + calories_list[1] + calories_list[2] << std::endl;

    return 0;
}