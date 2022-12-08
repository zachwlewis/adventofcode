// adventofcode.com
// Day 8
// https://adventofcode.com/2022/day/8

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <cstdio>
#include <set>
#include <sstream>
#include <map>

#define INPUT_FILE "inputs/d8.txt"

#define L 0
#define T 1
#define R 2
#define B 3

struct Tree
{
  int height = -1;
  bool visible[4] = {true, true, true, true};
  int max[4] = {-1, -1, -1, -1};
  int score[4] = {0, 0, 0, 0};

  void cmp(const Tree &other, size_t direction)
  {
    if (other.max[direction] >= height)
    {
      // tree is blocked in that direction
      visible[direction] = false;
      max[direction] = other.max[direction];
      return;
    }

    // tree is not blocked in that direction
    visible[direction] = true;
    max[direction] = height;
  }

  bool is_visible() const { return visible[L] || visible[T] || visible[R] || visible[B]; }
  int scenic_score() const { return score[L] * score[T] * score[R] * score[B]; }
};

int main() {

	std::ifstream input_file(INPUT_FILE);

	if (!input_file.is_open())
	{
		std::cout << "Unable to open input file: " << INPUT_FILE << std::endl;
		return 1;
	}

	size_t col = 0, row = 0;
	size_t score1 = 0;
	int score2 = 0;
  const Tree nulltree;

	std::vector<std::vector<Tree>> trees = {{}};

  char height;
	while (input_file.good())
	{
    char prev = height;
		input_file.get(height);
    if (height == '\n') continue;
    if (prev == '\n')
    {
      ++row;
      col = 0;
      trees.push_back({});
    }

    std::string s_height(1, height);
    Tree t;
    t.height = std::stoi(s_height);
    // While adding, we can check the top and left visibility of each tree.
    // Check left
    if (col == 0) t.cmp(nulltree, L);
    else t.cmp(trees[row][col-1], L);
    int ci = col;
    while (ci > 0)
    {
      ++t.score[L];
      if (t.height <= trees[row][ci-1].height) break;
      --ci;
    }
    

    // Check top
    if (row == 0) t.cmp(nulltree, T);
    else t.cmp(trees[row-1][col], T);

    int ri = row;
    while (ri > 0)
    {
      ++t.score[T];
      if (t.height <= trees[ri-1][col].height) break;
      --ri;
    }

    trees[row].push_back(t);
    ++col;
	}

  // Now, walk backwards and check the right and bottom visibility.
  const size_t M_COL = trees[0].size() - 1;
  const size_t M_ROW = trees.size() - 1;

  for (size_t r = M_ROW; r > 0; --r)
  {
    for (size_t c = M_COL; c > 0; --c)
    {
      Tree &t = trees[r][c];

      // Check right
      if (c == M_COL) t.cmp(nulltree, R);
      else t.cmp(trees[r][c+1], R);

      int ci = c;
      while (ci < M_COL)
      {
        ++t.score[R];
        if (t.height <= trees[r][ci+1].height) break;
        ++ci;
      }

      // Check bottom
      if (r == M_ROW) t.cmp(nulltree, B);
      else t.cmp(trees[r+1][c], B);

      int ri = r;
      while (ri < M_ROW)
      {
        ++t.score[B];
        if (t.height <= trees[ri+1][c].height) break;
        ++ri;
      }
    }
  }

  for (const auto &r : trees)
  {
    for (const auto &h : r)
    {
      int score = h.scenic_score();
      if (score > score2) score2 = score;
      if (h.is_visible())
      {
        ++score1;
        //std::cout << "\033[1m" << h.scenic_score() << "\033[0m";
      }
      //else std::cout << h.scenic_score();
    }
    //std::cout << std::endl;
  }

  //std::cout << M_COL + 1 << "x" << M_ROW + 1 << std::endl;

	std::cout << "Part 1: " << score1 << std::endl;
	std::cout << "Part 2: " << score2 << std::endl;

	return 0;
}
