package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
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
	return Answer(puzzleInput, 10)
}

func Answer2(puzzleInput string) int {
	return Answer(puzzleInput, 40)
}

// The rules to grow the polymer
// Example: map[BB:N BC:B] = put a N between B and B, put a B between B and C
type Rules = map[string]string

// The count of the characters in the polymer
// Example: [B:1749 C:298 H:161 N:865]
type CharCount = map[string]int

// Caching of the CharCount for speed-up
// Example: map[NBC2:map[B:4 N:2]] = growing NBC for 2 steps will give 4 extra B's and 2 N's
type Cache = map[string]map[string]int

func Answer(puzzleInput string, steps int) int {
	lines := strings.Split(puzzleInput, "\n")
	template := lines[0]
	rules := makeRules(lines)
	cache := Cache{}

	charCount := makeCharCount(template)
	charCount = merge(charCount, grow(template, steps, rules, cache))
	fmt.Println("After step", steps, "the character count is", charCount)

	most, least := mostAndLeast(charCount)
	return most - least
}

// Grow is a recursive function with caching
// It grows (a part of) a polymer until no more steps are left
// Then it continues to grow the other parts of the polymer
// It results in a count of the characters of the polymer
// Every subresult is saved in a cache to increase speed and preventing duplicate calculations
func grow(part string, steps int, rules Rules, cache Cache) CharCount {
	if steps == 0 {
		return CharCount{}
	}

	cacheKey := part + strconv.Itoa(steps)
	if charCount, ok := cache[cacheKey]; ok {
		return charCount
	}

	steps -= 1
	charCount := CharCount{}
	for i := 0; i < len(part)-1; i++ {
		start := string(part[i])
		end := string(part[i+1])
		if between, ok := rules[start+end]; ok {
			charCount[between] += 1
			charCount = merge(charCount, grow(start+between+end, steps, rules, cache))
		}
	}
	cache[cacheKey] = charCount

	return charCount
}

// Converts strings like "CH -> B" to map[CH:B]
func makeRules(lines []string) Rules {
	rules := Rules{}
	for i := 2; i < len(lines); i++ {
		line := lines[i]
		chars := strings.Split(line, "")
		startAndEnd := chars[0] + chars[1]
		between := chars[6]
		rules[startAndEnd] = between
	}
	return rules
}

func merge(charCount1 CharCount, charCount2 CharCount) CharCount {
	for char2, count2 := range charCount2 {
		charCount1[char2] += count2
	}
	return charCount1
}

func makeCharCount(str string) CharCount {
	charCount := CharCount{}
	for _, rune := range str {
		charCount[string(rune)] += 1
	}
	return charCount
}

func mostAndLeast(charCount CharCount) (int, int) {
	most := 0
	least := 0
	for _, count := range charCount {
		if count > most {
			most = count
		}
		if count < least || least == 0 {
			least = count
		}
	}
	return most, least
}
