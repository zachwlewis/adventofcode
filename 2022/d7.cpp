// adventofcode.com
// Day 7
// https://adventofcode.com/2022/day/7

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <cstdio>
#include <set>
#include <sstream>
#include <map>

#define INPUT_FILE "inputs/d7_sample.txt"

class File
{
public:
  File(std::string inName, char inMode, size_t inSize)
  : mName(inName), mMode(inMode), mSize(inSize) {}

  //static File mkdir(std::string inName) { return File(inName, 'd', 0); }
  //static File touch(std::string inName, size_t inSize) { return File(inName, '-', inSize); }

  
  std::map<std::string, File> children;
  File* mkdir(std::string inName)
  {
    children[inName] = File(inName, 'd', 0);
    return &children[inName];
  }
  File* touch(std::string inName, size_t inSize)
  {
    children[inName] = File(inName, '-', inSize);
    return &children[inName];
  }
  std::string_view name() const { return mName; }
  size_t size() const
  {
    if (!dir())
      return mSize;

    size_t dir_size = 0;
    for (auto file : children)
    {
      dir_size += file.second.size();
    }
    return dir_size;
  }
  bool dir() const { return mMode == 'd'; }
private:
  std::string mName = "";
  size_t mSize = 0;
  char mMode = '-';

};

std::string pwd(const std::vector<File*> &inPath)
{
  std::stringstream path;

  for (std::vector<File*>::const_iterator iter = inPath.begin(); iter < inPath.end(); ++iter)
  {
    path << "\033[34;7m" << (*iter)->name() << "\033[0m";
    path << "/";
  }

  return path.str();
}

void print_disk(const std::vector<File> &inDisk)
{
  for (auto iter = inDisk.begin(); iter < inDisk.end(); ++iter)
  {
    std::cout << (*iter).name() << " ";
    if ((*iter).dir()) 
      std::cout << "dir" << std::endl;
    else
     std::cout << (*iter).size() << std::endl;
  }
  
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

  std::string input = "";
  File root = File("/", 'd', 0);
  std::vector<File*> path = {&root};
  std::cout << pwd(path) << std::endl;
  File* dir = root.mkdir("one");
  root.touch("porn.jpg", 100);
  root.touch("taxes.pdf", 50);
  dir = root.mkdir("two");
  dir->touch("coin.png", 300);

  std::cout << root.size() << std::endl;

  // while (input_file.good())
  // {
  //   std::getline(input_file, input);
  //   std::cout << input << std::endl;
  // }

  std::cout << "Part 1: " << score1 << std::endl;  
  std::cout << "Part 2: " << score2 << std::endl;

  return 0;
}
