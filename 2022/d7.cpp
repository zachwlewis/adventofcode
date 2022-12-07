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

#define INPUT_FILE "inputs/d7.txt"

struct File
{
	std::string name = "unnamed";
	size_t size = 0;
	std::vector<File> contents = {};

	size_t get_size() const
	{
		// return size of file
		if (size != 0) return size;

		// return size of contents
		size_t calculated_size = 0;
		for (auto file : contents)
		{
			calculated_size += file.get_size();
		}
		return calculated_size;
	}
};

void print_tree(const File& inFile, size_t depth = 0)
{
	for (auto file : inFile.contents)
	{
		for (size_t i = 0; i < depth; ++i)
		{
			std::cout << "  ";
		}

		if (file.contents.size() > 0)
		{
			std::cout << "- " << file.name << " D (" << file.get_size() << ")" << std::endl;
			print_tree(file, depth + 1);
		}
		else std::cout << "- " << file.name << " F (" << file.get_size() << ")" << std::endl;
	}
}

void size_sum(const File& inFile, size_t& sum)
{
	//std::cout << inFile.name << " (" << sum << ")" << std::endl;
	for (auto file : inFile.contents)
	{
		if (file.contents.size() > 0)
		{
			// it's a directory: consider it.
			size_t size = file.get_size();
			if (size <= 100000)
			{
				sum += size;
				//std::cout << file.name << " (" << size << ") => " << sum << std::endl;
			}
				
			size_sum(file, sum);
		}
	}
}

void smallest_candidate(const File& inFile, size_t inSizeTarget, size_t &outSize)
{
	for (auto file : inFile.contents)
	{
		if (file.contents.size() > 0)
		{
			// it's a directory: consider it.
			size_t size = file.get_size();
			if (size >= inSizeTarget && size < outSize)
			{
				outSize = size;
				//std::cout << file.name << " (" << size << ")" << std::endl;
			}
				
			smallest_candidate(file, inSizeTarget, outSize);
		}
	}
}

int main() {

	std::ifstream input_file(INPUT_FILE);

	if (!input_file.is_open())
	{
		std::cout << "Unable to open input file: " << INPUT_FILE << std::endl;
		return 1;
	}

	const size_t TOTAL_SPACE = 70000000;
	const size_t REQUIRED_SPACE = 30000000;

	size_t line = 0;
	size_t score1 = 0;
	size_t score2 = TOTAL_SPACE;

	File disk = {"disk"};
	std::vector<File*> path = {&disk};
	File* current_directory = &disk;

	std::string input = "";

	while (input_file.good())
	{
		++line;
		std::vector<std::string> tokens;
		std::getline(input_file, input);
		//std::cout << line << ": " << input << std::endl;
		if (input.length() == 0)
			break;

		std::string buf;
		std::stringstream ss(input);
		while (ss >> buf)
		{
			tokens.push_back(buf);
		}
		
		if (tokens[0] == "$" && tokens[1] == "ls")
		{
			// ls
			//std::cout << "$ ls" << std::endl;
			continue;
		}

		if (tokens[0] == "$" && tokens[1] == "cd")
		{
			// cd
			if (tokens[2] == "..")
			{
				// navigate back
				//std::cout << "$ cd .." << std::endl;
				path.pop_back();
				current_directory = path.back();
				continue;
			}

			// switch working directory
			//std::cout << "$ cd " << tokens[2] << std::endl;
			current_directory->contents.push_back({tokens[2]});
			path.push_back(&current_directory->contents.back());
			current_directory = path.back();
			continue;
		}
		
		if (tokens[0] == "dir")
		{
			// add a directory
			//std::cout << "dir: " << tokens[1] << std::endl;
			continue;
		}

		if (size_t file_size = std::stoi(tokens[0]))
		{
			// add a file
			//std::cout << "file: " << tokens[1] << " (" << file_size << ")" << std::endl;
			current_directory->contents.push_back({tokens[1], file_size});
			continue;
		}

		//std::cout << "bad input" << std::endl;
	}

	// the disk has been populated.

	//print_tree(disk);
	//std::cout << "calc sum..." << std::endl;

	size_sum(disk, score1);
	std::cout << "Part 1: " << score1 << std::endl;


	size_t free_space = TOTAL_SPACE - disk.get_size();
	size_t size_target = REQUIRED_SPACE - free_space;
	//std::cout << "Free space: " << free_space << std::endl;
	//std::cout << "Size target: " << size_target << std::endl;
	smallest_candidate(disk, size_target, score2);
	std::cout << "Part 2: " << score2 << std::endl;

	return 0;
}
