// adventofcode.com
// Day 2
// https://adventofcode.com/2023/day/2

#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <map>
#include <algorithm>

#define INPUT_FILE "inputs/d2.txt"

std::vector<std::string> split(const std::string& s, char delimiter) {
    std::vector<std::string> tokens;
    std::string token;
    std::istringstream tokenStream(s);
    while (std::getline(tokenStream, token, delimiter))
    {
        tokens.push_back(token);
    }

    return tokens;
}

int main() {

	std::ifstream input_file (INPUT_FILE);
	std::string my_string;

	if (!input_file.is_open())
	{
		std::cout << "Unable to open input file: " << INPUT_FILE << std::endl;
		return 1;
	}

    std::map<std::string, int> MAX_COLORS = {
        {"red", 12},
        {"green", 13},
        {"blue", 14}
    };

	int answer1 = 0;
    int answer2 = 0;

	while (input_file)
	{
		std::string str;
		std::getline(input_file, str);
		if (str.empty()) break;
		
        // Split the game into two parts: [turn, pulls] 
        auto game = split(str, ':');
        
        // Get the turn id
        auto turn = split(game[0], ' ');
        int turn_id = std::stoi(turn[1]);
        
        // Get a list of pulls.
        auto pulls = split(game[1], ';');

        bool is_valid = true;
        std::map<std::string, int> min_cubes;
        // Check each pull for validity
        for (auto pull : pulls)
        {
            auto colors = split(pull, ',');
            for (auto sColor : colors)
            {
                auto value = split(sColor.substr(1), ' ');
                auto count = std::stoi(value[0]);
                auto color = value[1];
                if (count > MAX_COLORS[color]) {
                    is_valid = false;
                }

                // Determine the minimum required cubes.
                if (min_cubes[color] < count) min_cubes[color] = count;
            }
        }

        if (is_valid) {
            answer1 += turn_id;
        }

        int turn_power = min_cubes["red"] * min_cubes["blue"] * min_cubes["green"];
        answer2 += turn_power;
	}

	std::cout << "Answer 1: " << answer1 << std::endl;
	std::cout << "Answer 2: " << answer2 << std::endl;

	

	return 0;
}