// adventofcode.com
// Day 3
// https://adventofcode.com/2022/day/3

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <cstdio>
#include <set>

#define INPUT_FILE "inputs/d3.txt"

int item_priority(char inChar)
{
  // Lowercase item types a through z have priorities 1 through 26.
  // Uppercase item types A through Z have priorities 27 through 52.
  if (inChar >= 'a') return inChar - 'a' + 1;
  return inChar - 'A' + 27;
}

char shared_item(const std::string_view inRucksack)
{
  int mid = inRucksack.length() / 2;
  std::string a(inRucksack.begin(), inRucksack.begin() + mid);
  std::string b(inRucksack.end() - mid, inRucksack.end());

  std::sort(a.begin(), a.end());
  std::sort(b.begin(), b.end());

  std::string::iterator iter_a = a.begin();
  std::string::iterator iter_b = b.begin();

  while (*iter_a != *iter_b)
  {
    if (*iter_a < *iter_b) ++iter_a;
    else ++iter_b;
  }
  
  return *iter_a;
}

char badge_item(std::string &a, std::string &b, std::string &c)
{
  std::sort(a.begin(), a.end());
  std::sort(b.begin(), b.end());
  std::sort(c.begin(), c.end());

  std::string ab = "";
  std::string abc = "";
  std::set_intersection(a.begin(), a.end(), b.begin(), b.end(), std::back_inserter(ab));
  std::set_intersection(c.begin(), c.end(), ab.begin(), ab.end(), std::back_inserter(abc));

  return abc[0];
}

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
  std::string group[3];
  while (input_file)
  {
    std::string rucksack;
    std::getline(input_file, rucksack);

    if (rucksack.length() == 0)
      break;

    group[line_count % 3] = rucksack;
    
    ++line_count;
    
    char item = shared_item(rucksack);
    int priority = item_priority(item);
    score1 += priority;
    if (line_count % 3 != 0)
      continue;

    item = badge_item(group[0], group[1], group[2]);
    priority = item_priority(item);
    score2 += priority;
  }

  std::cout << "Lines: " << line_count << std::endl;
  std::cout << "Part 1: " << score1 << std::endl;
  std::cout << "Part 2: " << score2 << std::endl;
  return 0;
}
