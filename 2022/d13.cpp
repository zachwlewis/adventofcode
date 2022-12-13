// adventofcode.com
// Day 13
// https://adventofcode.com/2022/day/13

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <cstdio>
#include <set>
#include <sstream>
#include <memory>

#define INPUT_FILE "inputs/d13.txt"

struct Packet
{
  Packet()
  {
    num = 0;
    list = new std::vector<Packet>();
  }

  Packet(int inNum)
  {
    num = inNum;
    list = nullptr;
  }

  ~Packet()
  {
    if (list != nullptr)
      delete list;
  }

  // Copy ctor
  Packet(const Packet &p)
  {
    num = p.num;
    if (p.is_num())
      list = nullptr;
    else
      list = new std::vector<Packet>(*p.list);
  }

  //@name Members
  int num;
  std::vector<Packet>* list;
  
  //@name Functions
  Packet* add_list()
  {
    if (is_num())
    {
      std::cout << "Error: Attempting to add a list to a number packet!" << std::endl;
      return nullptr;
    }

    list->push_back({});
    return &list->back();
  }

  void add_num(int inNum)
  {
    if (is_num())
    {
      std::cout << "Error: Attempting to add a number to a number packet!" << std::endl;
      return;
    }
    list->emplace_back(inNum);
  }

  bool is_num() const { return list == nullptr; }


  std::string tostring() const
  {
    std::stringstream ss;
    if (is_num())
    {
      // just print the number if we're a number
      ss << num;
      return ss.str();
    }

    // step through children and print them.
    ss << "[";
    for (auto iter = list->begin(); iter < list->end(); ++iter)
    {
      ss << iter->tostring();
      if (iter != list->end() - 1)
        ss << ",";
    }
    ss << "]";

    return ss.str();
  }
};

int parse_int(const std::string_view inString, size_t start, size_t end)
{
  std::string numstr(inString.begin() + start, inString.begin() + end);
  return std::stoi(numstr);
}

Packet build_packet(const std::string_view inString)
{
  Packet p;
  std::vector<Packet*> packet_stack = { &p };
  const char* iter = inString.begin();
  int offset = -1;
  int loc = 0;
  for (auto iter = inString.begin() + 1; iter < inString.end(); ++iter)
  {
    ++loc;
    const char c = *iter;
    Packet* target = packet_stack.back();
    if (c == '[')
    {
      // starting a new list
      packet_stack.push_back(target->add_list());
    }
    else if (c == ']')
    {
      // closing current list
      if (offset != -1)
      {
        // we need to add a number before closing
        int value = parse_int(inString, offset, loc);
        target->add_num(value);
        offset = -1;
      }
      packet_stack.pop_back();
    }
    else if (c == ',')
    {
      if (offset != -1)
      {
        int value = parse_int(inString, offset, loc);
        target->add_num(value);
        offset = -1;
      }
    }
    else if (offset == -1)
    {
      // first number. Mark the location.
      offset = loc;
    }
  }

  return p;
}
int compare_nums(const Packet &lhs, const Packet &rhs)
{
  if (!lhs.is_num())
  {
    std::cout << "lhs is not a number!" << std::endl;
    return -1;
  }

  if (!rhs.is_num())
  {
    std::cout << "rhs is not a number!" << std::endl;
    return -1;
  }

  if (lhs.num < rhs.num) return 1;
  if (lhs.num > rhs.num) return -1;
  return 0;
}

int compare_packets(const Packet &lhs, const Packet &rhs)
{
  // check for trivial case, both packets are numbers.
  if (lhs.is_num() && rhs.is_num()) return compare_nums(lhs, rhs);
  if (lhs.is_num() && !rhs.is_num())
  {
    Packet p;
    p.add_num(lhs.num);
    return compare_packets(p, rhs);
  }
  if (!lhs.is_num() && rhs.is_num())
  {
    Packet p;
    p.add_num(rhs.num);
    return compare_packets(lhs, p);
  }

  // they are both lists. iterate the lists
  const size_t l_count = lhs.list->size();
  const size_t r_count = rhs.list->size();
  const size_t count = std::max<size_t>(l_count, r_count);
  for (size_t i = 0; i < count; ++i)
  {
    if (i >= l_count) return 1;  // lhs ran out of items first
    if (i >= r_count) return -1; // rhs ran out of items first

    // both still have items
    Packet &left = lhs.list->at(i);
    Packet &right = rhs.list->at(i);

    int cmp = compare_packets(left, right);
    if (cmp != 0) return cmp;
  }
  
  return 0;
}

int main() {

	std::ifstream input_file(INPUT_FILE);
  std::vector<Packet> packets;
  Packet divider_a = build_packet("[[2]]");
  Packet divider_b = build_packet("[[6]]");
  packets.push_back(divider_a);
  packets.push_back(divider_b);

	if (!input_file.is_open())
	{
		std::cout << "Unable to open input file: " << INPUT_FILE << std::endl;
		return 1;
	}

	size_t score1 = 0;
	size_t score2 = 0;
  size_t packet_index = 1;
	while (input_file.good())
	{
    std::string left_packet;
    std::string right_packet;
    std::getline(input_file, left_packet);
    if (left_packet == "") break;
    std::getline(input_file, right_packet);

    Packet left = build_packet(left_packet);
    Packet right = build_packet(right_packet);
    packets.push_back(left);
    packets.push_back(right);

    bool correct_order = compare_packets(left, right) > 0;
    if (correct_order)
      score1 += packet_index;

    ++packet_index;
	}

  // sort the packets
  std::vector<Packet*> sorting = {};

  for (Packet &p : packets)
    sorting.push_back(&p);

  std::sort(sorting.begin(), sorting.end(), [](Packet* lhs, Packet* rhs) {
    return compare_packets(*lhs, *rhs) == 1;
  });

  size_t pa, pb, idx = 1;
  for (Packet *p : sorting)
  {
    if (p->tostring() == "[[2]]") pa = idx;
    if (p->tostring() == "[[6]]") pb = idx;
    ++idx;
  }

  score2 = pa * pb;
 	
	std::cout << "Part 1: " << score1 << std::endl;
	std::cout << "Part 2: " << score2 << std::endl;

	return 0;
}
