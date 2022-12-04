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
	polymer := getTemplate(lines)
	rules := getRules(lines)
	// fmt.Println(polymer)
	// fmt.Println(rules)

	for i := 1; i <= 10; i++ {
		polymer = growPolymer(polymer, rules)
		// fmt.Println("Step", i, polymer)
	}

	countMost, countLeast := countMostAndLeastCommonElement(polymer)
	return countMost - countLeast
}

func Answer2(puzzleInput string) int {
	lines := strings.Split(puzzleInput, "\n")
	polymer := getTemplate(lines)
	rules := getRules(lines)
	// fmt.Println(polymer)
	// fmt.Println(rules)

	countMost, countLeast := 0, 0
	for i := 1; i <= 40; i++ {
		polymer = growPolymer(polymer, rules)
		countMost, countLeast = countMostAndLeastCommonElement(polymer)
		fmt.Println("Step", i, countMost, countLeast)
	}

	return countMost - countLeast
}

type keyValue struct {
	Key   string
	Value int
}

func countMostAndLeastCommonElement(polymer []string) (int, int) {
	charCount := getCharCount(polymer)

	var sortSlice []keyValue
	for key, value := range charCount {
		sortSlice = append(sortSlice, keyValue{key, value})
	}

	sort.Slice(sortSlice, func(i, j int) bool {
		return sortSlice[i].Value > sortSlice[j].Value
	})

	countMost := sortSlice[0].Value
	countLeast := sortSlice[len(sortSlice)-1].Value
	return countMost, countLeast
}

func getCharCount(polymer []string) map[string]int {
	charCount := map[string]int{}
	for _, char := range polymer {
		if count, ok := charCount[char]; ok {
			charCount[char] = count + 1
		} else {
			charCount[char] = 1
		}
	}
	return charCount
}

func growPolymer(polymer []string, rules [][]string) []string {
	newPolymer := []string{}
	for i := 0; i < len(polymer)-1; i++ {
		char1 := polymer[i]
		char2 := polymer[i+1]
		newPolymer = append(newPolymer, char1)
		for _, rule := range rules {
			if char1 == rule[0] && char2 == rule[1] {
				newPolymer = append(newPolymer, rule[2])
				break
			}
		}
		if i == len(polymer)-2 {
			newPolymer = append(newPolymer, char2)
		}
	}
	return newPolymer
}

func getRules(lines []string) [][]string {
	rules := [][]string{}
	for i := 2; i < len(lines); i++ {
		line := lines[i]
		chars := strings.Split(line, "")
		rule := []string{chars[0], chars[1], chars[6]}
		rules = append(rules, rule)
	}
	return rules
}

func getTemplate(lines []string) []string {
	line := lines[0]
	template := strings.Split(line, "")
	return template
}
