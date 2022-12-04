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
	rules1 := getRules(lines)
	rules5 := growRulesInSteps(rules1, 4)
	polymer = growPolymerInSteps(polymer, rules5, 2)
	countMost, countLeast := countMostAndLeastCommonElement(polymer)
	return countMost - countLeast
}

func Answer2(puzzleInput string) int {
	lines := strings.Split(puzzleInput, "\n")
	polymer := getTemplate(lines)
	rules1 := getRules(lines)
	rules10 := growRulesInSteps(rules1, 5)
	polymer = growPolymerInSteps(polymer, rules10, 3)
	countMost, countLeast := countMostAndLeastCommonElement(polymer)
	return countMost - countLeast

	return 2188189693529
}

func growRulesInSteps(rules [][]string, steps int) [][]string {
	newRules := [][]string{}
	for _, rule := range rules {
		newRule := growRuleInSteps(rule, rules, steps)
		newRules = append(newRules, newRule)
		// fmt.Println("Rule step", steps, newRule)
	}
	return newRules
}

func growRuleInSteps(rule []string, rules [][]string, steps int) []string {
	ruleAsPolymer := strings.Join(rule, "")
	ruleAsPolymer = growPolymerInSteps(ruleAsPolymer, rules, steps)
	chars := strings.Split(ruleAsPolymer, "")
	newRule := []string{
		chars[0],
		strings.Join(chars[1:len(chars)-1], ""),
		chars[len(chars)-1],
	}
	return newRule
}

func growPolymerInSteps(polymer string, rules [][]string, steps int) string {
	for step := 1; step <= steps; step++ {
		polymer = growPolymer(polymer, rules)
		fmt.Println("Polymer step", step, len(polymer))
	}
	return polymer
}

func growPolymer(polymer string, rules [][]string) string {
	newPolymer := ""

	// Loop through the polymer in pairs
	for i := 0; i < len(polymer)-1; i++ {
		polyLeft := string(polymer[i])
		polyRight := string(polymer[i+1])

		// Left
		newPolymer += polyLeft

		// Find rule and apply
		for _, rule := range rules {
			ruleLeft, ruleAdd, ruleRight := rule[0], rule[1], rule[2]
			ruleApplies := polyLeft == ruleLeft && polyRight == ruleRight
			if ruleApplies {
				newPolymer += ruleAdd
				break
			}
		}
	}
	// Right: add the right character only at the end of the polymer
	newPolymer += string(polymer[len(polymer)-1])
	return newPolymer
}

func countMostAndLeastCommonElement(polymer string) (int, int) {
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

func getCharCount(polymer string) map[string]int {
	charCount := map[string]int{}
	for _, rune := range polymer {
		char := string(rune)
		if count, ok := charCount[char]; ok {
			charCount[char] = count + 1
		} else {
			charCount[char] = 1
		}
	}
	return charCount
}

func getRules(lines []string) [][]string {
	rules := [][]string{}
	for i := 2; i < len(lines); i++ {
		line := lines[i]
		chars := strings.Split(line, "")
		rule := []string{chars[0], chars[6], chars[1]}
		rules = append(rules, rule)
	}
	return rules
}

func getTemplate(lines []string) string {
	// template := strings.Split(lines[0], "")
	template := lines[0]
	return template
}

func printStepAndPolymer(step int, polymer []string) {
	fmt.Printf("Step %v ", step)
	for _, char := range polymer {
		fmt.Printf("%v", char)
	}
	fmt.Println()
}

type keyValue struct {
	Key   string
	Value int
}
