// adventofcode.com
// Day 5: Seed Planting
// https://adventofcode.com/2023/day/5

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

#define INPUT_FILE "inputs/d5_sample.txt"

struct SeedTransform {
	uint64_t source_start;
	uint64_t destination_start;
	uint64_t length;
};

inline std::ostream & operator<<(std::ostream & Str, SeedTransform const & v) { 
	Str << "[" << v.source_start << ".." << v.source_start + v.length-1 << "] => [" << v.destination_start << ".." << v.destination_start + v.length << "]";
	return Str;
}

/**
 * Transforms the seed id according to the given transform.
 * @param seedId The seed id to transform.
 * @param transform The transform to apply.
 * @return True if the seed id was transformed, false otherwise.
*/
bool transformSeed(uint64_t &seedId, const SeedTransform& transform) {
	if (seedId >= transform.source_start && seedId < transform.source_start + transform.length) {
		seedId = transform.destination_start + (seedId - transform.source_start);
		return true;
	}
	return false;
}

/**
 * Transforms a range into a list of ranges.
 * @param range The range to transform.
 * @param transform The transform to apply.
 * @return A list of transformed ranges.
 */
std::vector<Range<uint64_t>> transformRange(const Range<uint64_t>& range, const SeedTransform& transform) {
	std::vector<Range<uint64_t>> result;
	// #TODO
	return result;
}

/**
 * Transforms the seed id according to the given transforms.
 * @param seedId The seed id to transform.
 * @param transforms The transforms to apply.
 * @return True if the seed id was transformed, false otherwise.
*/
bool mapSeed(uint64_t &seedId, const std::vector<SeedTransform>& transforms) {
	for (auto& transform : transforms) {
		if (transformSeed(seedId, transform)) return true;
	}
	return false;
}

uint64_t parseSeedMap(std::ifstream& input_file, std::vector<SeedTransform>& seed_map) {
	std::string str;
	std::getline(input_file, str); // title line
	std::getline(input_file, str);
	while(!str.empty()) {
		std::vector<std::string> parts = split(str, ' ');
		uint64_t destination = std::stoull(parts[0]);
		uint64_t source = std::stoull(parts[1]);
		uint64_t length = std::stoull(parts[2]);
		seed_map.push_back({source, destination, length});
		std::getline(input_file, str);
	}

	return seed_map.size() - 1;
}

int main() {

	std::ifstream input_file (INPUT_FILE);

	if (!input_file.is_open())
	{
		std::cout << "Unable to open input file: " << INPUT_FILE << std::endl;
		return 1;
	}

	uint64_t answer1 = 0;
	uint64_t answer2 = 0;

	std::vector<uint64_t> seedIds;
	std::vector<Range<uint64_t>> seedRanges;

	std::vector<SeedTransform> seed_to_soil;
	std::vector<SeedTransform> soil_to_fertilizer;
	std::vector<SeedTransform> fertilizer_to_water;
	std::vector<SeedTransform> water_to_light;
	std::vector<SeedTransform> light_to_temperature;
	std::vector<SeedTransform> temperature_to_humidity;
	std::vector<SeedTransform> humidity_to_location;

	std::string str;
	
	{
		// seed: <seed_ids>
		std::getline(input_file, str);
		std::vector<std::string> seed_ids = split(str, ' ');
		for (int i = 1; i < seed_ids.size(); ++i) {
			std::cout << "Seed ID: " << seed_ids[i] << std::endl;
			seedIds.push_back(std::stol(seed_ids[i]));
		}

		// also parse seed ranges now
		for (int i = 1; i < seed_ids.size(); i += 2) {
			Range<uint64_t> range = Range<uint64_t>::fromLength(std::stoull(seed_ids[i]), std::stoull(seed_ids[i+1]));
			std::cout << "Seed Range: " << range << std::endl;
			seedRanges.push_back(range);
		}
	}

	std::getline(input_file, str); // blank line
	parseSeedMap(input_file, seed_to_soil);
	// std::getline(input_file, str); // blank line
	parseSeedMap(input_file, soil_to_fertilizer);
	// std::getline(input_file, str); // blank line
	parseSeedMap(input_file, fertilizer_to_water);
	// std::getline(input_file, str); // blank line
	parseSeedMap(input_file, water_to_light);
	// std::getline(input_file, str); // blank line
	parseSeedMap(input_file, light_to_temperature);
	// std::getline(input_file, str); // blank line
	parseSeedMap(input_file, temperature_to_humidity);
	// std::getline(input_file, str); // blank line
	parseSeedMap(input_file, humidity_to_location);


	uint64_t lowest = UINT_FAST64_MAX;
	for (auto& seedId : seedIds) {
		// std::cout << "Seed ID: " << seedId << " => ";
		mapSeed(seedId, seed_to_soil);
		// std::cout << seedId << " => ";
		mapSeed(seedId, soil_to_fertilizer);
		// std::cout << seedId << " => ";
		mapSeed(seedId, fertilizer_to_water);
		// std::cout << seedId << " => ";
		mapSeed(seedId, water_to_light);
		// std::cout << seedId << " => ";
		mapSeed(seedId, light_to_temperature);
		// std::cout << seedId << " => ";
		mapSeed(seedId, temperature_to_humidity);
		// std::cout << seedId << " => ";
		mapSeed(seedId, humidity_to_location);
		// std::cout << seedId << std::endl;

		if (seedId < lowest) {
			lowest = seedId;
		}

	}
	answer1 = lowest;
	std::cout << "Answer 1: " << answer1 << std::endl;
	std::cout << "Answer 2: " << answer2 << std::endl;

	return 0;
}