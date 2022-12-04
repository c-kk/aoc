package main

import (
	"fmt"
	"io/ioutil"
	"sort"
	"strings"
)

func main() {
	bytes, _ := ioutil.ReadFile("data.txt")
	puzzleInput := string(bytes)
	fmt.Println(Answer1(puzzleInput))
	fmt.Println(Answer2(puzzleInput))
}

func Answer1(puzzleInput string) int {
	lines := strings.Split(puzzleInput, "\n")
	template := getTemplate(lines)
	fmt.Println("Temp", template)
	rules := getRules(lines)

	steps := 10
	charCount := map[string]int{}
	charCount = mergeCharCounts(charCount, growAndCount(template, rules, steps))
	charCount = mergeCharCounts(charCount, makeCharCount(template))
	fmt.Println("After step", steps, "CharCount", charCount)

	countMost, countLeast := mostAndLeast(charCount)
	return countMost - countLeast
}

func growAndCount(part string, rules map[string]string, steps int) map[string]int {
	// fmt.Println(steps, part)
	charCount := map[string]int{}

	if steps == 0 {
		return charCount
	}

	if len(part) > 2 {
		for index := 0; index < len(part)-1; index++ {
			startChar := string(part[index])
			endChar := string(part[index+1])
			subPart := startChar + endChar
			charCount = mergeCharCounts(charCount, growAndCount(subPart, rules, steps))
		}
	}

	if len(part) == 2 {
		startChar := string(part[0])
		endChar := string(part[1])
		newPart := startChar
		toFind := part
		//charCount = mergeCharCounts(charCount, makeCharCount(startChar))
		if addBetween, ok := rules[toFind]; ok {
			newPart += addBetween
			charCount = mergeCharCounts(charCount, makeCharCount(addBetween))
			steps -= 1
		} else {
			steps = 0
		}
		newPart += endChar
		charCount = mergeCharCounts(charCount, growAndCount(newPart, rules, steps))
	}

	// fmt.Println(steps, "CharCount", charCount)
	return charCount
}

// func countPaths(cave int, seen int, allowDoubleVisit int, cache map[int]int, neighbours map[int][]int) int {
// 	if cave == END_CAVE_ID {
// 		return 1
// 	}

// 	if cave >= MIN_SMALL_CAVE_ID {
// 		if seen%cave == 0 {
// 			if allowDoubleVisit == -1 {
// 				return 0
// 			}
// 			allowDoubleVisit = -1
// 		} else {
// 			seen *= cave
// 		}
// 	}

// 	total := 0
// 	for _, neighbour := range neighbours[cave] {
// 		count := countPaths(neighbour, seen, allowDoubleVisit, cache, neighbours)
// 		total += count
// 	}
// 	return total
// }

func mergeCharCounts(charCount1 map[string]int, charCount2 map[string]int) map[string]int {
	for char2, count2 := range charCount2 {
		if _, ok := charCount1[char2]; ok {
			charCount1[char2] += count2
		} else {
			charCount1[char2] = count2
		}
	}
	return charCount1
}

func makeCharCount(str string) map[string]int {
	charCount := map[string]int{}
	for _, rune := range str {
		char := string(rune)
		if count, ok := charCount[char]; ok {
			charCount[char] = count + 1
		} else {
			charCount[char] = 1
		}
	}
	return charCount
}

func mostAndLeast(charCount map[string]int) (int, int) {
	var sortSlice []keyValue
	for key, value := range charCount {
		sortSlice = append(sortSlice, keyValue{key, value})
	}

	sort.Slice(sortSlice, func(i, j int) bool {
		return sortSlice[i].Value > sortSlice[j].Value
	})

	if len(sortSlice) < 2 {
		return 0, 0
	}

	countMost := sortSlice[0].Value
	countLeast := sortSlice[len(sortSlice)-1].Value
	return countMost, countLeast
}

func getRules(lines []string) map[string]string {
	rules := map[string]string{}
	for i := 2; i < len(lines); i++ {
		line := lines[i]
		chars := strings.Split(line, "")
		toFind := chars[0] + chars[1]
		addBetween := chars[6]
		rules[toFind] = addBetween
	}
	return rules
}

func getTemplate(lines []string) string {
	template := lines[0]
	return template
}

type keyValue struct {
	Key   string
	Value int
}

func Answer2(puzzleInput string) int {
	return 0
	//return 2188189693529
}
