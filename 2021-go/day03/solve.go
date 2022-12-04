package main

import (
	"fmt"
	"io/ioutil"
	"math"
	"strconv"
	"strings"
)

func main() {
	bytes, _ := ioutil.ReadFile("data.txt")
	puzzleInput := string(bytes)
	fmt.Println(Answer1(puzzleInput))
	fmt.Println(Answer2(puzzleInput))
}

func Answer1(puzzleInput string) int {
	lines := strings.Split(string(puzzleInput), "\n")
	sums := make([]int, len(lines[0]))

	for _, line := range lines {
		for j, character := range line {
			if string(character) == "1" {
				sums[j] += 1
			}
		}
	}
	gamma := 0
	epsilon := 0

	for j, sum := range sums {
		position := len(sums) - j - 1

		if sum > len(lines)/2 {
			gamma += int(math.Exp2(float64(position)))
		} else {
			epsilon += int(math.Exp2(float64(position)))
		}
	}

	return gamma * epsilon
}

func Answer2(puzzleInput string) int {
	lines := strings.Split(string(puzzleInput), "\n")
	var oxygen int64
	var scrubber int64

	position := 0
	sum := 0
	currentLines := lines
	var newLines0 []string
	var newLines1 []string

	for {
		for _, line := range currentLines {
			if string(line[position]) == "1" {
				sum += 1
				newLines1 = append(newLines1, line)
			} else {
				newLines0 = append(newLines0, line)
			}
		}

		position += 1
		if len(newLines1) >= len(newLines0) {
			currentLines = newLines1
		} else {
			currentLines = newLines0
		}
		newLines0 = newLines0[:0]
		newLines1 = newLines1[:0]
		if len(currentLines) == 1 {
			oxygen, _ = strconv.ParseInt(currentLines[0], 2, 64)
			break
		}
	}

	position = 0
	sum = 0
	currentLines = lines

	for {
		for _, line := range currentLines {
			if string(line[position]) == "1" {
				sum += 1
				newLines1 = append(newLines1, line)
			} else {
				newLines0 = append(newLines0, line)
			}
		}

		position += 1
		if len(newLines1) >= len(newLines0) {
			currentLines = newLines0
		} else {
			currentLines = newLines1
		}
		newLines0 = newLines0[:0]
		newLines1 = newLines1[:0]
		if len(currentLines) == 1 {
			scrubber, _ = strconv.ParseInt(currentLines[0], 2, 64)
			break
		}
	}

	return int(oxygen * scrubber)
}
