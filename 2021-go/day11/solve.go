package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

const (
	FLASHED = 11
)

func main() {
	bytes, _ := ioutil.ReadFile("data.txt")
	puzzleInput := string(bytes)
	fmt.Println(Answer1(puzzleInput))
	fmt.Println(Answer2(puzzleInput))
}

func Answer1(puzzleInput string) int {
	lines := strings.Split(puzzleInput, "\n")
	field := convertStringSliceToIntSlices(lines)
	flashes := 0
	stepFlashes := 0

	for step := 1; step <= 100; step++ {
		field, stepFlashes = runStep(field)
		flashes += stepFlashes
		printField(field)
		fmt.Println("Step", step, "Flashes total", flashes, "Flashes in step", stepFlashes)
	}

	return flashes
}

func Answer2(puzzleInput string) int {
	lines := strings.Split(puzzleInput, "\n")
	field := convertStringSliceToIntSlices(lines)
	flashes := 0
	stepFlashes := 0
	stepThatAllOctopusesFlash := 0

	for step := 1; step <= 10000; step++ {
		field, stepFlashes = runStep(field)
		flashes += stepFlashes
		printField(field)
		fmt.Println("Step", step, "Flashes total", flashes, "Flashes in step", stepFlashes)

		if stepFlashes == 100 {
			stepThatAllOctopusesFlash = step
			break
		}
	}

	return stepThatAllOctopusesFlash
}

func runStep(field [][]int) ([][]int, int) {
	stepFlashes := 0
	field = increaseEnergyByOne(field)
	field, stepFlashes = keepFlashingOctopuses(field)
	field = resetFlashedOctopuses(field)
	return field, stepFlashes
}

func resetFlashedOctopuses(field [][]int) [][]int {
	for y, row := range field {
		for x := range row {
			val := field[x][y]
			if val == FLASHED {
				field[x][y] = 0
			}
		}
	}
	return field
}

func keepFlashingOctopuses(field [][]int) ([][]int, int) {
	flashes := 0
	newFlashes := 0

	for {
		field, newFlashes = flashOctopuses(field)
		flashes += newFlashes
		if newFlashes == 0 {
			break
		}
	}
	return field, flashes
}

func flashOctopuses(field [][]int) ([][]int, int) {
	ySize := len(field)
	xSize := len(field[0])
	count := 0

	for y, row := range field {
		for x := range row {
			val := field[x][y]
			if val == 10 {
				count += 1
				field[x][y] = FLASHED
				for ny := y - 1; ny <= y+1; ny++ {
					for nx := x - 1; nx <= x+1; nx++ {
						if nx >= 0 && nx < xSize && ny >= 0 && ny < ySize {
							nval := field[nx][ny]
							if nval <= 9 {
								field[nx][ny] += 1
							}
						}
					}
				}
			}
		}
	}

	return field, count
}

func increaseEnergyByOne(field [][]int) [][]int {
	for y, row := range field {
		for x := range row {
			field[x][y] += 1
		}
	}
	return field
}

func printField(field [][]int) {
	for _, row := range field {
		for _, item := range row {
			extraSpace := ""
			if item < 10 {
				extraSpace = " "
			}
			fmt.Printf("%v%v", extraSpace, item)
		}
		fmt.Println("")
	}
}

func convertStringSliceToIntSlices(stringSlice []string) [][]int {
	var intSlices [][]int
	for _, str := range stringSlice {
		var intSlice []int
		for _, rune := range str {
			int, _ := strconv.Atoi(string(rune))
			intSlice = append(intSlice, int)
		}
		intSlices = append(intSlices, intSlice)
	}
	return intSlices
}
