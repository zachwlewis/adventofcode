// adventofcode.com
// Day 2
// https://adventofcode.com/2022/day/2

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <cstdio>

enum class Throw : int { Rock = 1, Paper = 2, Scissors = 3 };
const int IN_OFFSET = (int)'A' - 1;
const int OUT_OFFSET = (int)'X' - 1;

/**
 * Does throw inA beat inB?
 * @returns Throw score of player A.
 */
int score_throw(Throw inA, Throw inB)
{
  if (inA == inB) return (int)inA + 3;
  if ((inA == Throw::Rock && inB == Throw::Scissors)
  ||  (inA == Throw::Paper && inB == Throw::Rock)
  ||  (inA == Throw::Scissors && inB == Throw::Paper)) return (int)inA + 6;
  return (int)inA;
}

Throw get_play(const std::string_view value)
{
  if (value == "A X") return Throw::Scissors;
  if (value == "A Y") return Throw::Rock;
  if (value == "A Z") return Throw::Paper;
  if (value == "B X") return Throw::Rock;
  if (value == "B Y") return Throw::Paper;
  if (value == "B Z") return Throw::Scissors;
  if (value == "C X") return Throw::Paper;
  if (value == "C Y") return Throw::Scissors;
  if (value == "C Z") return Throw::Rock;
  return Throw::Rock;
}

int main() {
    std::ifstream input_file ("inputs/d2.txt");
    std::string my_string;

    if (!input_file.is_open())
    {
      std::cout << "Unable to open input!" << std::endl;
      return 1;
    }


    std::string round;
    int score = 0;
    int score2 = 0;
    Throw me, opponent;
    while (input_file)
    {
      std::getline(input_file, round);
      if (round.length() == 0)
        break;

      opponent = (Throw)((int)round[0] - IN_OFFSET);
      me = (Throw)((int)round[2] - OUT_OFFSET);
      score += score_throw(me, opponent);

      me = get_play(round);
      score2 += score_throw(me, opponent);
    }

    std::cout << "Part 1: " << score << std::endl;
    std::cout << "Part 2: " << score2 << std::endl;

    return 0;
}
