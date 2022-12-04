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

func Answer1(puzzleInput string) int {
	lines := strings.Split(puzzleInput, "\n")
	xSize := getSize(lines, "x")
	fmt.Println("xSize", xSize)
	return 17
}

func getSize(lines []string, axis string) int {
	for _, line := range lines {
		fmt.Println(line, strings.HasPrefix(line, "fold along x"))
	}
	return 100
}

func Answer2(puzzleInput string) int {
	// lines := strings.Split(puzzleInput, "\n")

	return 0
}
