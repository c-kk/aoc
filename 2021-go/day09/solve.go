package main

import (
	"fmt"
	"io/ioutil"
	"sort"
	"strconv"
	"strings"
)

func main() {
	bytes, _ := ioutil.ReadFile("data.txt")
	puzzleInput := string(bytes)
	fmt.Println(Answer1(puzzleInput))
	fmt.Println(Answer2(puzzleInput))
}

type point struct {
	y   int
	x   int
	val int
}

func Answer1(puzzleInput string) int {
	lines := strings.Split(puzzleInput, "\n")
	field := convertStringSliceToIntSlices(lines)
	for _, row := range field {
		fmt.Println("Field row", row)
	}

	lowPoints := findLowPoints(field)

	count := 0
	for _, lowPoint := range lowPoints {
		count += lowPoint.val + 1
	}

	return count
}

func Answer2(puzzleInput string) int {
	lines := strings.Split(puzzleInput, "\n")
	field := convertStringSliceToIntSlices(lines)
	lowPoints := findLowPoints(field)
	lakes := [][]point{}

	for _, lowPoint := range lowPoints {
		lakePointsDone := []point{}
		lakePointsToCheck := []point{}
		lakePointsToCheck = append(lakePointsToCheck, lowPoint)

		for len(lakePointsToCheck) > 0 {
			foundLakePoints := []point{}
			for _, lakePointToCheck := range lakePointsToCheck {
				y := lakePointToCheck.y
				x := lakePointToCheck.x
				field[y][x] = 9

				if y > 0 {
					y2 := y - 1
					x2 := x
					above := field[y2][x2]
					if above < 9 {
						foundLakePoints = append(foundLakePoints, point{y2, x2, above})
						field[y2][x2] = 9
					}
				}
				if y < len(field)-1 {
					y2 := y + 1
					x2 := x
					below := field[y2][x2]
					if below < 9 {
						foundLakePoints = append(foundLakePoints, point{y2, x2, below})
						field[y2][x2] = 9
					}
				}
				if x > 0 {
					y2 := y
					x2 := x - 1
					left := field[y2][x2]
					if left < 9 {
						foundLakePoints = append(foundLakePoints, point{y2, x2, left})
						field[y2][x2] = 9
					}
				}
				if x < len(field[y])-1 {
					y2 := y
					x2 := x + 1
					right := field[y2][x2]
					if right < 9 {
						foundLakePoints = append(foundLakePoints, point{y2, x2, right})
						field[y2][x2] = 9
					}
				}

				lakePointsDone = append(lakePointsDone, lakePointToCheck)
			}
			lakePointsToCheck = foundLakePoints
		}
		lakes = append(lakes, lakePointsDone)
		fmt.Println("Lake", lowPoint, lakePointsDone, len(lakePointsDone))
	}

	lakeSizes := []int{}
	for _, lake := range lakes {
		lakeSizes = append(lakeSizes, len(lake))
	}
	sort.Ints(lakeSizes)
	biggestLakeSizes := lakeSizes[len(lakeSizes)-3:]
	fmt.Println("Biggest lake sizes", biggestLakeSizes)

	answer := 1
	for _, lakeSize := range biggestLakeSizes {
		answer *= lakeSize
	}

	return answer
}

func findLowPoints(field [][]int) []point {
	lowPoints := []point{}
	for y, row := range field {
		for x, val := range row {
			above := 9
			below := 9
			left := 9
			right := 9
			if y > 0 {
				y2 := y - 1
				x2 := x
				above = field[y2][x2]
			}
			if y < len(field)-1 {
				y2 := y + 1
				x2 := x
				below = field[y2][x2]
			}
			if x > 0 {
				y2 := y
				x2 := x - 1
				left = field[y2][x2]
			}
			if x < len(row)-1 {
				y2 := y
				x2 := x + 1
				right = field[y2][x2]
			}
			if val < above && val < below && val < left && val < right {
				lowPoint := point{y, x, val}
				lowPoints = append(lowPoints, lowPoint)
				fmt.Println("Low point", y, x, val)
			}
		}
	}
	return lowPoints
}

// Convert a string slice to int slices
// Example: ["2199943210", "3987894921"] to [[2 1 9 9 9 4 3 2 1 0][3 9 8 7 8 9 4 9 2 1]]
func convertStringSliceToIntSlices(strings []string) [][]int {
	var intSlices [][]int
	for _, str := range strings {
		var intSlice []int
		for _, rune := range str {
			int, _ := strconv.Atoi(string(rune))
			intSlice = append(intSlice, int)
		}
		intSlices = append(intSlices, intSlice)
	}
	return intSlices
}
