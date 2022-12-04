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

type cave struct {
	key     string
	size    string
	visited bool
	targets []*cave
}

func (t cave) String() string {
	targetKeys := []string{}
	for _, target := range t.targets {
		targetKeys = append(targetKeys, target.key)
	}
	return fmt.Sprintf("{%v %v %v %v}", t.key, t.size, t.visited, targetKeys)
}

type Path struct {
	caveKeys []string
}

func Answer1(puzzleInput string) int {
	lines := strings.Split(puzzleInput, "\n")
	caves := convertLinesToCaves(lines)
	printCaves(caves)

	paths := [][]string{}
	path := []string{"start"}
	paths = append(paths, path)
	printPaths(paths)

	oldPathCount := 1
	step := 0

	for step < 3 {
		fmt.Println("###### STEP", step, "######")

		newPaths := [][]string{}

		for _, path := range paths {
			fmt.Println("Path:", path)

			caveKey := path[len(path)-1]
			cave := caves[caveKey]
			targets := filterTargets(cave.targets, path)
			fmt.Println("Targets:", targets)

			if len(targets) == 0 {
				fmt.Println("No allowed target found")
				fmt.Println()
				newPaths = append(newPaths, path)
			} else {
				for index, target := range targets {
					fmt.Println("Index", index, "Target", target)
					newPath := append(path, target.key)

					newPaths = append(newPaths, newPath)
				}
			}

			printPaths(newPaths)
		}

		// 	currentCave := caves["start"]
		// 	path := []string{}
		// 	path = append(path, currentCave.key)

		// 	for {
		// 		currentCave.visited = true
		// 		// fmt.Println("Current cave:", currentCave.key, currentCave)

		// 		paths := append(validPaths, invalidPaths...)
		// 		targets := filterTargets(currentCave.targets, path, paths)
		// 		// fmt.Println("Targets:", targets)

		// 		if len(targets) == 0 {
		// 			// fmt.Println("No allowed target found")
		// 			// fmt.Println("Path:", path)
		// 			// fmt.Println()
		// 			if !doesPathExist(path, invalidPaths) {
		// 				invalidPaths = append(invalidPaths, path)
		// 			}
		// 			path = []string{}
		// 			break
		// 		}

		// 		target := targets[0]
		// 		path = append(path, target.key)

		// 		if target.key == "end" {
		// 			// fmt.Println("End of path reached")
		// 			// fmt.Println("Path:", path)
		// 			// fmt.Println()
		// 			validPaths = append(validPaths, path)
		// 			path = []string{}
		// 			break
		// 		}

		// 		// fmt.Println("Selected target:", target)
		// 		// fmt.Println("Path:", path)
		// 		// fmt.Println()
		// 		currentCave = target
		// 	}

		// 	// fmt.Println("Valid paths:", validPaths)
		// 	// fmt.Println("Invalid paths:", invalidPaths)
		// 	validPathCount := len(validPaths)
		// 	invalidPathCount := len(invalidPaths)

		// 	fmt.Println("Step", step, "Valid paths", validPathCount)
		// 	// fmt.Println()

		newPathCount := len(newPaths)
		if newPathCount == oldPathCount {
			break
		}
		paths = newPaths
		oldPathCount = newPathCount
		step += 1
	}

	return 10
}

func printPaths(paths [][]string) {
	fmt.Println("Paths:")
	for _, path := range paths {
		fmt.Println(path)
	}
}

// Return only the targets that are allowed to go to
func filterTargets(targets []*cave, path []string) []*cave {
	filtered := []*cave{}
	for _, target := range targets {
		// It's not allowed if target is small and visited
		if target.size == "small" {
			visited := false
			for _, caveKey := range path {
				if target.key == caveKey {
					visited = true
				}
			}
			if visited {
				continue
			}

		}

		filtered = append(filtered, target)
	}
	return filtered
}

// Check if the path exists to prevent duplicate paths
func doesPathExist(path []string, paths [][]string) bool {
	exists := false
	for _, existingPath := range paths {
		pathString := strings.Join(path, ",")
		existingPathString := strings.Join(existingPath, ",")
		if pathString == existingPathString {
			exists = true
		}
	}
	return exists
}

func printCaves(caves map[string]*cave) {
	fmt.Println("Caves:")
	for _, cave := range caves {
		fmt.Println(cave)
	}
}

func convertLinesToCaves(lines []string) map[string]*cave {
	caves := map[string]*cave{}

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

			caves[caveKey] = &cave{caveKey, size, false, []*cave{}}
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
			caveFrom.targets = append(caveFrom.targets, caves[to])
		}

		// Reverse the route: also add the 'from' location to the 'to' cave destinations
		// Restrictions: you can't reverse from the end and you can't go back to the start
		if to != "end" && from != "start" {
			caveTo.targets = append(caveTo.targets, caveFrom)
		}
	}
	return caves
}

func Answer2(puzzleInput string) int {
	// lines := strings.Split(puzzleInput, "\n")
	return 0
}
