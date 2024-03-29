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
	fmt.Println("Solution for 2021 day 12 using Breadth-first search (BFS)")
	fmt.Println(Answer1(puzzleInput))
	fmt.Println(Answer2(puzzleInput))
	fmt.Println("Time elapsed", time.Since(start))
}

func Answer1(puzzleInput string) int {
	return countPossiblePaths(puzzleInput, 0)
}

func Answer2(puzzleInput string) int {
	return countPossiblePaths(puzzleInput, 1)
}

func countPossiblePaths(puzzleInput string, maxDoubleVisits int) int {
	lines := strings.Split(puzzleInput, "\n")
	caves := convertLinesToCaves(lines)
	activePaths := append([][]int{}, []int{START_CAVE_ID})
	countFinishedPaths := 0

	for len(activePaths) > 0 {
		newPaths := [][]int{}

		for _, activePath := range activePaths {
			caveId := activePath[len(activePath)-1]
			if caveId == END_CAVE_ID {
				countFinishedPaths += 1
				continue
			}

			// Start cave, end cave and big caves don't need to be stored in the path
			if caveId < 0 {
				activePath = activePath[:len(activePath)-1]
			}

			targets := caves[caveId]
			targets = filterTargets(targets, activePath, maxDoubleVisits)

			for key, targetId := range targets {
				if key == len(targets)-1 {
					newPath := append(activePath, targetId)
					newPaths = append(newPaths, newPath)
				} else {
					newPath := append([]int{}, activePath...)
					newPath = append(newPath, targetId)
					newPaths = append(newPaths, newPath)
				}
			}
		}

		activePaths = newPaths
	}
	return countFinishedPaths
}

func filterTargets(targets []int, path []int, maxDoubleVisits int) []int {
	filtered := []int{}
	for _, targetId := range targets {
		if isAllowed(targetId, path, maxDoubleVisits) {
			filtered = append(filtered, targetId)
		}
	}
	return filtered
}

// Always allow big targets. Small target can only be visited once or twice
func isAllowed(targetId int, path []int, maxDoubleVisits int) bool {
	if targetId < 0 {
		return true
	}
	countDoubleVisits := 0
	multiple := targetId
	for _, caveId := range path {
		if multiple%caveId == 0 {
			countDoubleVisits += 1
			if countDoubleVisits > maxDoubleVisits {
				return false
			}
		} else {
			multiple *= caveId
		}
	}
	return true
}

// Small caves have positive id's, the other caves have negative id's
// Using primes as id's for small caves, for simplifying finding duplicates in isAllowed function
const START_CAVE_ID int = -100
const END_CAVE_ID int = -101

func convertLinesToCaves(lines []string) map[int][]int {
	bigCaveId := -200
	smallCaveId := 0
	primes := []int{2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541}
	caves := map[int][]int{}
	idLookup := map[string]int{}

	for _, line := range lines {
		caveKeys := strings.Split(line, "-")
		for _, caveKey := range caveKeys {
			if _, ok := idLookup[caveKey]; !ok {
				caveId := 0
				if caveKey == "start" {
					caveId = START_CAVE_ID
				} else if caveKey == "end" {
					caveId = END_CAVE_ID
				} else if caveKey[0] > 90 { // Lowercase is > 90 (A = 65, Z = 90, a = 97, z = 122)
					caveId = primes[smallCaveId]
					smallCaveId += 1
				} else {
					caveId = bigCaveId
					bigCaveId -= 1
				}
				caves[caveId] = []int{}
				idLookup[caveKey] = caveId
			}
		}

		fromId, toId := idLookup[caveKeys[0]], idLookup[caveKeys[1]]

		// Add 'to' location to 'from' cave destinations. Can't go to start or exit from the end
		if toId != START_CAVE_ID && fromId != END_CAVE_ID {
			caves[fromId] = append(caves[fromId], toId)
		}

		// Reverse: add 'from' location to 'to' cave destinations. Can't reverse from the end or go back to start
		if toId != END_CAVE_ID && fromId != START_CAVE_ID {
			caves[toId] = append(caves[toId], fromId)
		}
	}
	return caves
}
