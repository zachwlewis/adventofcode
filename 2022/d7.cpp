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
	File() : mName(""), mMode('d'), mSize(0) {}
	File(std::string inName, char inMode, size_t inSize)
		: mName(inName), mMode(inMode), mSize(inSize) {}
	const static char DIR_FLAG = 'd';
	const static char FILE_FLAG = '-';
	static File mkdir(std::string inName) { return File(inName, File::DIR_FLAG, 0); }
	static File touch(std::string inName, size_t inSize) { return File(inName, File::FILE_FLAG, inSize); }

	std::vector<File*> children;
	std::string_view name() const { return mName; }
	size_t size() const
	{
		if (is_file())
			return mSize;

		size_t dir_size = 0;
		for (auto file : children)
		{
			dir_size += file->size();
		}
		return dir_size;
	}
	bool is_dir() const { return mMode == File::DIR_FLAG; }
	bool is_file() const { return mMode == File::FILE_FLAG; }
private:
	std::string mName = "";
	size_t mSize = 0;
	char mMode = '-';

};

void pwd(const std::vector<File*>& inPath)
{
	for (auto file : inPath)
	{
		std::cout << "\033[34;7m" << file->name() << "\033[0m";
		std::cout << "/";
	}

	std::cout << std::endl;
}

void print_disk(const std::vector<File>& inDisk)
{
	for (auto iter = inDisk.begin(); iter < inDisk.end(); ++iter)
	{
		std::cout << (*iter).name() << " ";
		if ((*iter).is_dir())
			std::cout << "dir" << std::endl;
		else
			std::cout << (*iter).size() << std::endl;
	}
}

int main() {

	std::ifstream input_file(INPUT_FILE);

	if (!input_file.is_open())
	{
		std::cout << "Unable to open input file: " << INPUT_FILE << std::endl;
		return 1;
	}

	int score1 = 0;
	int score2 = 0;

	std::vector<File> disk = {};
	std::vector<File*> path = {};

	std::string input = "";

	while (input_file.good())
	{
		std::vector<std::string> tokens;
		std::getline(input_file, input);
		if (input.length() == 0)
			break;

		std::string buf;
		std::stringstream ss(input);
		while (ss >> buf)
		{
			tokens.push_back(buf);
		}
		
		if (tokens[0] == "$")
		{
			// new command for working directory
			std::cout << "command: " << tokens[1] << std::endl;
			continue;
		}
		
		if (tokens[0] == "dir")
		{
			// add a directory
			std::cout << "new directory: " << tokens[1] << std::endl;
			continue;
		}

		if (size_t file_size = std::stoi(tokens[0]))
		{
			// add a file
			std::cout << "new file: " << tokens[1] << " (" << file_size << ")" << std::endl;
			continue;
		}

		std::cout << "bad input" << std::endl;
	}

	std::cout << "Part 1: " << score1 << std::endl;
	std::cout << "Part 2: " << score2 << std::endl;

	return 0;
}
