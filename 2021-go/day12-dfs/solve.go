// Very fast solution (< 0.3ms)
// Inspired by Reddit user 4HbQ. See: https://old.reddit.com/r/adventofcode/comments/rehj2r/2021_day_12_solutions/ho7x83o/
// Added:
// * primes as id's for the caves from very fast lookups and logic checks (from 300ms to 10ms)
// * caching (from 10ms to 0.3ms)

package main

import (
	"fmt"
	"io/ioutil"
	"strings"
	"time"
)

func main() {
	bytes, _ := ioutil.ReadFile("data.txt")
	puzzleInput := string(bytes)
	start := time.Now()
	fmt.Println("Solution for 2021 day 12 using Depth-first search (DFS)")
	fmt.Printf("%v\n%v\nTime elapsed %v\n", Answer(puzzleInput, -1), Answer(puzzleInput, 1), time.Since(start))
}

func Answer(puzzleInput string, allowDoubleVisit int) int {
	lines := strings.Split(puzzleInput, "\n")
	neighbours := convertLinesToNeighbours(lines)
	cave := START_CAVE_ID
	seen := cave
	cache := map[int]int{}
	return countPaths(cave, seen, allowDoubleVisit, cache, neighbours)
}

func countPaths(cave int, seen int, allowDoubleVisit int, cache map[int]int, neighbours map[int][]int) int {
	if cave == END_CAVE_ID {
		return 1
	}

	if cave >= MIN_SMALL_CAVE_ID {
		if seen%cave == 0 {
			if allowDoubleVisit == -1 {
				return 0
			}
			allowDoubleVisit = -1
		} else {
			seen *= cave
		}
	}

	total := 0
	for _, neighbour := range neighbours[cave] {
		cacheKey := (neighbour + 1) * seen * allowDoubleVisit
		count, ok := cache[cacheKey]
		if !ok {
			count = countPaths(neighbour, seen, allowDoubleVisit, cache, neighbours)
			cache[cacheKey] = count
		}
		total += count
	}
	return total
}

func convertLinesToNeighbours(lines []string) map[int][]int {
	bigCavePrimeIndex := 1
	smallCavePrimeIndex := 21
	neighbours := map[int][]int{}
	idLookup := map[string]int{}

	for _, line := range lines {
		caveNames := strings.Split(line, "-")
		for _, caveName := range caveNames {
			caveId, ok := idLookup[caveName]
			if !ok {
				caveId, bigCavePrimeIndex, smallCavePrimeIndex = getCaveId(caveName, bigCavePrimeIndex, smallCavePrimeIndex)
				idLookup[caveName] = caveId
				neighbours[caveId] = []int{}
			}
		}

		fromId := idLookup[caveNames[0]]
		toId := idLookup[caveNames[1]]

		// Add 'to' location to 'from' cave destinations. Can't go back to start or exit from the end
		if toId != START_CAVE_ID && fromId != END_CAVE_ID {
			neighbours[fromId] = append(neighbours[fromId], toId)
		}

		// Reverse: add 'from' location to 'to' cave destinations. Can't reverse from the end or go back to start
		if toId != END_CAVE_ID && fromId != START_CAVE_ID {
			neighbours[toId] = append(neighbours[toId], fromId)
		}
	}
	return neighbours
}

const START_CAVE_ID int = 1
const END_CAVE_ID int = 2
const MIN_SMALL_CAVE_ID int = 79 // The prime at index 21 is 79

func getCaveId(caveName string, bigCavePrimeIndex int, smallCavePrimeIndex int) (int, int, int) {
	primes := []int{2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541}
	caveId := 0
	if caveName == "start" {
		caveId = START_CAVE_ID
	} else if caveName == "end" {
		caveId = END_CAVE_ID
	} else if caveName[0] > 90 { // Lowercase is > 90 (A = 65, Z = 90, a = 97, z = 122)
		caveId = primes[smallCavePrimeIndex]
		smallCavePrimeIndex += 1
	} else {
		caveId = primes[bigCavePrimeIndex]
		bigCavePrimeIndex += 1
	}
	return caveId, bigCavePrimeIndex, smallCavePrimeIndex
}
