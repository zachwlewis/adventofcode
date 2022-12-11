// adventofcode.com
// Day 11
// https://adventofcode.com/2022/day/11

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <cstdio>
#include <set>
#include <sstream>
#include <map>

#define INPUT_FILE "inputs/d11.txt"

struct Monkey
{
  Monkey() {}
  Monkey(std::vector<size_t> inItems, const std::string_view inOperation, int inTest, size_t inTrue, size_t inFalse)
  : items(inItems),
    operation(inOperation),
    test(inTest),
    branch_true(inTrue),
    branch_false(inFalse)
    {}
  std::vector<size_t> items = {};
  std::string operation = "";
  size_t test = 0;
  size_t branch_true = 0;
  size_t branch_false = 0;
  size_t inspections = 0;
};

/**
 * @brief Updates worry using logical techniques.
 */
void gain_worry(const std::string_view inOperation, size_t &ioWorry)
{
  size_t val = ioWorry;
  if (inOperation[6] != 'o')
  {
    std::string v_str(inOperation.begin() + 6, inOperation.end());
    val = std::stoi(v_str);
  }

  if (inOperation[4] == '+') ioWorry += val;
  if (inOperation[4] == '*') ioWorry *= val;
}

/**
 * @brief Updates worry using value-reduction techniques.
 * @details To prevent the numbers from getting huge and rolling over, inTest
 * is used to reduce the actual size while retaining testability (when inTest is a
 * common multiple of all testable items).
 */
void gain_worry2(const std::string_view inOperation, size_t &ioWorry, size_t inTest)
{
  size_t val = ioWorry;
  ioWorry = ioWorry % inTest;
  if (inOperation[6] != 'o')
  {
    std::string v_str(inOperation.begin() + 6, inOperation.end());
    val = std::stoi(v_str);
  }

  if (inOperation[4] == '+') ioWorry += val;
  if (inOperation[4] == '*') ioWorry *= val;
  
}

void decay_worry(size_t &ioWorry) { ioWorry /= 3; }

size_t part1(std::vector<Monkey> inMonkeys)
{
  for (size_t round = 0; round < 20; ++round)
  {
    for (size_t idx = 0; idx < inMonkeys.size(); ++idx)
    {
      Monkey &m = inMonkeys[idx];
      for (size_t item : m.items)
      {
        // 1. Inspect item and increase worry
        m.inspections++;
        gain_worry(m.operation, item);
        // 2. Reduce worry
        decay_worry(item);
        // 3. Throw item based on condition
        if (item % m.test == 0) inMonkeys[m.branch_true].items.push_back(item);
        else inMonkeys[m.branch_false].items.push_back(item);
      }
      m.items.clear();
    }
  }

  // Get top two monkey inspectors
  std::vector<size_t> inspections = {};
  for (const Monkey &m : inMonkeys)
  {
    inspections.push_back(m.inspections);
  }

  std::sort(inspections.begin(), inspections.end(), std::greater<size_t>());
  return inspections[0] * inspections[1];
}

size_t part2(std::vector<Monkey> inMonkeys)
{
  // Determine a common multiple for all tests to use when reducing large numbers.
  size_t lcm = 1;
  for (const Monkey& m : inMonkeys) lcm *= m.test;

  for (size_t round = 0; round < 10000; ++round)
  {
    for (size_t idx = 0; idx < inMonkeys.size(); ++idx)
    {
      Monkey &m = inMonkeys[idx];
      for (size_t item : m.items)
      {
        // 1. Inspect item and increase worry
        m.inspections++;
        gain_worry2(m.operation, item, lcm);
        // 2. Throw item based on condition
        if (item % m.test == 0) inMonkeys[m.branch_true].items.push_back(item);
        else inMonkeys[m.branch_false].items.push_back(item);
      }
      m.items.clear();
    }
  }

  // Get top two monkey inspectors
  std::vector<size_t> inspections = {};
  for (const Monkey &m : inMonkeys)
    inspections.push_back(m.inspections);

  std::sort(inspections.begin(), inspections.end(), std::greater<size_t>());
  return inspections[0] * inspections[1];
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
  std::string s_items, s_operation, s_test, s_true, s_false;
  std::vector<Monkey> monkeys = {};
	while (input_file.good())
	{
    std::getline(input_file, s_items);
    if (s_items == "") break;
    std::getline(input_file, s_operation);
    std::getline(input_file, s_test);
    std::getline(input_file, s_true);
    std::getline(input_file, s_false);

    std::stringstream ss(s_items);
    std::vector<size_t> items = {};
    std::string vv;
    while (std::getline(ss, vv, ' '))
      items.push_back(std::stoi(vv));

    
    monkeys.emplace_back(items, s_operation, std::stoi(s_test), std::stoi(s_true), std::stoi(s_false));
	}

  // monkeys have been populated
  // time for monkey business
  score1 = part1(monkeys);
  score2 = part2(monkeys);
 	
	std::cout << "Part 1: " << score1 << std::endl;
	std::cout << "Part 2: " << score2 << std::endl;

	return 0;
}
