package main

import (
	"fmt"
	"io/ioutil"
	"strings"
	"strconv"
)

func main() {
	bytes, _ := ioutil.ReadFile("data.txt")
	puzzleInput := string(bytes)
	fmt.Println(Answer1(puzzleInput))
	fmt.Println(Answer2(puzzleInput))
}

func Answer1(puzzleInput string) int {
	lines := strings.Split(puzzleInput, "\n")
	field := convertStringSlicesToIntSlices(lines)
	for _, row := range field {
		fmt.Println(row)
	}

	count := 0
	for y, row := range field {
		for x, val := range row {
			// fmt.Println(y, x, val)
			above := 9
			below := 9
			left := 9
			right := 9
			if y > 0 {
				above = field[y-1][x]
			} 
			if y < len(field) - 1 {
				below = field[y+1][x]
			}
			if x > 0 {
				left = field[y][x-1]
			} 
			if x < len(row) - 1 {
				right = field[y][x+1]
			}
			if val < above && val < below && val < left && val < right {
				count += val + 1
				fmt.Println("Low point", y, x, val, count)
			} 
		}
	}

	return count
}

func convertStringSlicesToIntSlices(strings []string) [][]int {
	var intsSlice [][]int
	for _, str := range strings {
		var ints []int
		for _, rune := range str {
			int, _ := strconv.Atoi(string(rune))
			ints = append(ints, int)
		}
		intsSlice = append(intsSlice, ints)
	}
	return intsSlice
}

func Answer2(puzzleInput string) int {
	return 1134
}
