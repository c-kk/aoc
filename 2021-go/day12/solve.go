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
	fmt.Println(Answer1(puzzleInput))
	fmt.Println(Answer2(puzzleInput))
	fmt.Println("Time elapsed", time.Since(start))
}

func Answer1(puzzleInput string) int {
	allowOneDoubleVisit := false
	return countPossiblePaths(puzzleInput, allowOneDoubleVisit)
}

func Answer2(puzzleInput string) int {
	allowOneDoubleVisit := true
	return countPossiblePaths(puzzleInput, allowOneDoubleVisit)
}

func countPossiblePaths(puzzleInput string, allowOneDoubleVisit bool) int {
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

			targets := caves[caveId]
			targets = filterTargets(targets, activePath, allowOneDoubleVisit)

			if len(targets) > 0 {
				for _, targetId := range targets {
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

// Always allow big targets and check small targets
func filterTargets(targets []int, path []int, allowOneDoubleVisit bool) []int {
	filtered := []int{}
	for _, targetId := range targets {
		if targetId > 100 || isAllowed(targetId, path, allowOneDoubleVisit) {
			filtered = append(filtered, targetId)
		}
	}
	return filtered
}

// A small target is not allowed if it's already visited
// In part B one double visit is allowed
func isAllowed(targetId int, path []int, allowOneDoubleVisit bool) bool {
	found := map[int]bool{}
	found[targetId] = true
	countDoubleVisits := 0
	for _, caveId := range path[1:] {
		// Only check for previous double visits in small caves
		if caveId >= 100 {
			continue
		}

		if found[caveId] {
			countDoubleVisits += 1
			if countDoubleVisits == 1 && !allowOneDoubleVisit {
				return false
			}
			if countDoubleVisits == 2 {
				return false
			}
		} else {
			found[caveId] = true
		}
	}
	return true
}

const START_CAVE_ID int = 100
const END_CAVE_ID int = 101

// Convert input to caves
func convertLinesToCaves(lines []string) map[int][]int {
	smallCaveId := 0
	bigCaveId := 200

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
					// A = 65, Z = 90, a = 97, z = 122, lowercase is > 90
				} else if caveKey[0] > 90 {
					caveId = smallCaveId
					smallCaveId += 1
				} else {
					caveId = bigCaveId
					bigCaveId += 1
				}
				caves[caveId] = []int{}
				idLookup[caveKey] = caveId
			}
		}

		fromId, toId := idLookup[caveKeys[0]], idLookup[caveKeys[1]]

		// Add the 'to' location to the 'from' cave destinations
		// Restrictions: you can't go the start or exit from the end
		if toId != START_CAVE_ID && fromId != END_CAVE_ID {
			caves[fromId] = append(caves[fromId], toId)
		}

		// Reverse the route: also add the 'from' location to the 'to' cave destinations
		// Restrictions: you can't reverse from the end and you can't go back to the start
		if toId != END_CAVE_ID && fromId != START_CAVE_ID {
			caves[toId] = append(caves[toId], fromId)
		}
	}
	return caves
}
