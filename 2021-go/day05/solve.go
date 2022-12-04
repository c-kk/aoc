package main

import (
	"fmt"
	"io/ioutil"
	"regexp"
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
	lines := strings.Split(puzzleInput, "\n")

	dy := len(lines) * 2
	dx := len(lines) * 2
	field := make([][]int, dy)
	for y := range field {
		field[y] = make([]int, dx)
	}

	for _, line := range lines {
		numStrings := regexp.MustCompile(`,| -> `).Split(line, 4)
		nums := convertToInts(numStrings)

		x1 := nums[0]
		y1 := nums[1]
		x2 := nums[2]
		y2 := nums[3]

		xRange := createRange(x1, x2)
		yRange := createRange(y1, y2)

		isHorizont := len(yRange) == 1
		isVertical := len(xRange) == 1

		if isHorizont {
			for _, x := range xRange {
				field[y1][x] += 1
			}
		}

		if isVertical {
			for _, y := range yRange {
				field[y][x1] += 1
			}
		}
	}

	printField(field)
	return countHigherThanOneInField(field)
}

func Answer2(puzzleInput string) int {
	lines := strings.Split(puzzleInput, "\n")

	dy := len(lines) * 2
	dx := len(lines) * 2
	field := make([][]int, dy)
	for y := range field {
		field[y] = make([]int, dx)
	}

	for _, line := range lines {
		numStrings := regexp.MustCompile(`,| -> `).Split(line, 4)
		nums := convertToInts(numStrings)

		x1 := nums[0]
		y1 := nums[1]
		x2 := nums[2]
		y2 := nums[3]

		xRange := createRange(x1, x2)
		yRange := createRange(y1, y2)

		isHorizont := len(yRange) == 1
		isVertical := len(xRange) == 1
		isDiagonal := len(xRange) == len(yRange)

		if isHorizont {
			for _, x := range xRange {
				field[y1][x] += 1
			}
		}

		if isVertical {
			for _, y := range yRange {
				field[y][x1] += 1
			}
		}

		if isDiagonal {
			for i, x := range xRange {
				y := yRange[i]
				field[y][x] += 1
			}
		}
	}

	printField(field)
	return countHigherThanOneInField(field)
}

func createRange(start int, end int) []int {
	delta := end - start
	direction := 1

	if delta < 0 {
		direction = -1
	}

	var rnge []int
	for a := start; a != end+direction; a += direction {
		rnge = append(rnge, a)
	}
	return rnge
}

func printField(field [][]int) {
	for _, row := range field {
		for _, item := range row {
			fmt.Print(item)
		}
		fmt.Println()
	}
}

func countHigherThanOneInField(field [][]int) int {
	count := 0
	for _, row := range field {
		for _, item := range row {
			if item > 1 {
				count += 1
			}
		}
	}
	return count
}

func convertToInts(numStrings []string) []int {
	var numInts []int
	for _, numString := range numStrings {
		numInt, _ := strconv.Atoi(numString)
		numInts = append(numInts, numInt)
	}
	return numInts
}

func min(x, y int) int {
	if x < y {
		return x
	}
	return y
}

func max(x, y int) int {
	if x > y {
		return x
	}
	return y
}
