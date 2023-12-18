// adventofcode.com
// Day 6: Boat Race
// https://adventofcode.com/2023/day/6

#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <map>
#include <algorithm>
#include <format>
#include "stringtools.hpp"
#include "range.hpp"

//#define SAMPLE

struct RaceData {
	/** The length of the race in milliseconds. */
	uint64_t time;

	/** The record distance. */
	uint64_t distance;
};

uint64_t getTotalDistance(uint64_t chargeTime, uint64_t raceTime) {
	// chargeTime is our velocity
	int travelTime = raceTime - chargeTime;
	return chargeTime * travelTime;
}

int main() {

	int answer1 = 1;
	int answer2 = 0;

#ifdef SAMPLE
	std::vector<RaceData> races({{7, 9}, {15, 40}, {30, 200}});
	RaceData mainEvent = {71530, 940200};
#else
	std::vector<RaceData> races({{52, 426}, {94, 1374}, {75, 1279}, {94, 1216}});
	RaceData mainEvent = {52947594, 426137412791216};
#endif

	for (const RaceData& race : races) {
		int wins = 0;
		for (uint64_t i = 0; i <= race.time; ++i) {
			uint64_t distance = getTotalDistance(i, race.time);
			if (distance > race.distance) ++wins;
		}

		std::cout << "Wins: " << wins << std::endl;
		answer1 *= wins;
	}

	for (uint64_t i = 0; i <= mainEvent.time; ++i) {
			uint64_t distance = getTotalDistance(i, mainEvent.time);
			if (distance > mainEvent.distance) ++answer2;
		}

	std::cout << "Answer 1: " << answer1 << std::endl;
	std::cout << "Answer 2: " << answer2 << std::endl;

	return 0;
}