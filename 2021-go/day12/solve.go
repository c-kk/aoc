package main

import (
	"fmt"
	"io/ioutil"
	"strings"
)

func main() {
	bytes, _ := ioutil.ReadFile("data.txt")
	puzzleInput := string(bytes)
	fmt.Println(Answer1(puzzleInput))
	fmt.Println(Answer2(puzzleInput))
}

type Cave struct {
	key string
	size    string
	targets []Cave
}

type Path struct {
	caveKeys []string
}

func Answer1(puzzleInput string) int {
	lines := strings.Split(puzzleInput, "\n")
	caves := convertLinesToCaves(lines)
	// printCaves(caves)
	finishedPaths := [][]string{}
	activePaths := append([][]string{}, []string{"start"})

	doubleVisited := true
	step := 0
	subStep := 0

	for {
		newActivePaths := [][]string{}

		for _, activePath := range activePaths {
			subStep += 1
			caveKey := activePath[len(activePath)-1]
			if caveKey == "end" {
				finishedPaths = append(finishedPaths, activePath)
			}

			cave := caves[caveKey]
			targets, _ := filterTargets(cave.targets, activePath, doubleVisited)

			if len(targets) > 0 {
				for _, target := range targets {
					newActivePath := append([]string{}, activePath...)
					newActivePath = append(newActivePath, target.key)
					newActivePaths = append(newActivePaths, newActivePath)
				}
			}
		}

		fmt.Println("Step", step, "Substeps", subStep, "Finished paths", len(finishedPaths), "Active paths", len(newActivePaths))

		if len(newActivePaths) == 0 {
			break
		}

		activePaths = newActivePaths
		step += 1
	}

	return len(finishedPaths)
}

func Answer2(puzzleInput string) int {
	lines := strings.Split(puzzleInput, "\n")
	caves := convertLinesToCaves(lines)
	// printCaves(caves)
	finishedPaths := [][]string{}
	activePaths := append([][]string{}, []string{"start"})

	step := 0
	subStep := 0

	for {
		newActivePaths := [][]string{}

		for _, activePath := range activePaths {
			doubleVisited := false
			subStep += 1
			caveKey := activePath[len(activePath)-1]
			if caveKey == "end" {
				finishedPaths = append(finishedPaths, activePath)
			}

			cave := caves[caveKey]

			targets := []Cave{}
			targets, doubleVisited = filterTargets(cave.targets, activePath, doubleVisited)

			if len(targets) > 0 {
				for _, target := range targets {
					newActivePath := append([]string{}, activePath...)
					newActivePath = append(newActivePath, target.key)
					newActivePaths = append(newActivePaths, newActivePath)
				}
			}
		}

		fmt.Println("Step", step, "Substeps", subStep, "Finished paths", len(finishedPaths), "Active paths", len(newActivePaths))

		if len(newActivePaths) == 0 {
			break
		}

		activePaths = newActivePaths
		step += 1
	}

	return len(finishedPaths)
}

// Convert input to caves
func convertLinesToCaves(lines []string) map[string]Cave {
	caves := map[string]Cave{}

	// Create caves
	for _, line := range lines {
		caveKeys := strings.Split(line, "-")
		for _, caveKey := range caveKeys {
			size := "small"
			if strings.ToUpper(caveKey) == caveKey {
				size = "big"
			}
			if caveKey == "start" || caveKey == "end" {
				size = "nil"
			}

			caves[caveKey] = Cave{caveKey, size, []Cave{}}
		}
	}

	// Find destinations which you can reach from the specific cave
	for _, line := range lines {
		caveKeys := strings.Split(line, "-")
		from := caveKeys[0]
		to := caveKeys[1]
		caveFrom := caves[from]
		caveTo := caves[to]

		// Add the 'to' location to the 'from' cave destinations
		// Restrictions: you can't go the start or exit from the end
		if to != "start" && from != "end" {
			caveFrom.targets = append(caveFrom.targets, caveTo)
			caves[from] = caveFrom
		}

		// Reverse the route: also add the 'from' location to the 'to' cave destinations
		// Restrictions: you can't reverse from the end and you can't go back to the start
		if to != "end" && from != "start" {
			caveTo.targets = append(caveTo.targets, caveFrom)
			caves[to] = caveTo
		}
	}
	return caves
}

// Return only the targets that are allowed to go to
func filterTargets(targets []Cave, path []string, doubleVisited bool) ([]Cave, bool) {
	filtered := []Cave{}
	for _, target := range targets {
		// It's not allowed if target is small and visited
		if target.size == "small" {
			visited := false
			for _, caveKey := range path {
				if target.key == caveKey {
					if doubleVisited == false {
						doubleVisited = true
					} else {
						visited = true
					}
				}
			}
			if visited {
				continue
			}
		}

		filtered = append(filtered, target)
	}
	return filtered, doubleVisited
}

func printPaths(paths [][]string) {
	fmt.Println("Paths:")
	for _, path := range paths {
		fmt.Println(path)
	}
}

func printCaves(caves map[string]Cave) {
	fmt.Println("Caves:")
	for _, cave := range caves {
		fmt.Println(cave)
	}
}