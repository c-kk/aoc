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
	lines := strings.Split(puzzleInput, "\n")
	ySize := getSize(lines, "y")
	xSize := getSize(lines, "x")
	paper := makeEmptyPaper(ySize, xSize)
	paper = fillPaper(paper, lines)
	folds := getFolds(lines)
	paper = doFold(paper, folds[0])
	count := countVisible(paper)
	return count
}

func Answer2(puzzleInput string) int {
	lines := strings.Split(puzzleInput, "\n")
	ySize := getSize(lines, "y")
	xSize := getSize(lines, "x")
	paper := makeEmptyPaper(ySize, xSize)
	paper = fillPaper(paper, lines)
	folds := getFolds(lines)
	for _, fold := range folds {
		paper = doFold(paper, fold)
	}
	printPaper(paper)
	count := countVisible(paper)
	return count
}

func getSize(lines []string, axis string) int {
	for _, line := range lines {
		splitted := strings.Split(line, "=")
		if strings.HasPrefix(splitted[0], "fold along "+axis) {
			max, _ := strconv.Atoi(splitted[1])
			size := 1 + max*2
			return size
		}
	}
	return 0
}

func makeEmptyPaper(ySize int, xSize int) [][]int {
	paper := make([][]int, ySize)
	for i := 0; i < ySize; i++ {
		paper[i] = make([]int, xSize)
	}
	return paper
}

func fillPaper(paper [][]int, lines []string) [][]int {
	for _, line := range lines {
		if line == "" || strings.HasPrefix(line, "fold") {
			continue
		}
		splitted := strings.Split(line, ",")
		x, _ := strconv.Atoi(splitted[0])
		y, _ := strconv.Atoi(splitted[1])
		paper[y][x] = 1
	}
	return paper
}

func getFolds(lines []string) []string {
	folds := []string{}
	for _, line := range lines {
		if strings.Contains(line, "y") {
			folds = append(folds, "y")
		}
		if strings.Contains(line, "x") {
			folds = append(folds, "x")
		}
	}
	return folds
}

func doFold(paper [][]int, fold string) [][]int {
	ySize := len(paper)
	xSize := len(paper[0])

	newYSize := ySize / 2
	newXSize := xSize

	if fold == "x" {
		newYSize = ySize
		newXSize = xSize / 2
	}

	newPaper := makeEmptyPaper(newYSize, newXSize)

	for y, row := range paper {
		for x, val := range row {
			if val == 1 {
				newY := y
				newX := x
				if newY > newYSize-1 {
					newY = -newY + ySize - 1
				}
				if newX > newXSize-1 {
					newX = -newX + xSize - 1
				}
				newPaper[newY][newX] = val
			}

		}
	}

	return newPaper
}

func countVisible(paper [][]int) int {
	count := 0
	for _, row := range paper {
		for _, val := range row {
			count += val
		}
	}
	return count
}

func printPaper(paper [][]int) {
	for y, row := range paper {
		for _, val := range row {
			char := "."
			if val == 1 {
				char = "#"
			}
			fmt.Printf("%v", char)
		}
		fmt.Printf(" %v\n", y)
	}
}
