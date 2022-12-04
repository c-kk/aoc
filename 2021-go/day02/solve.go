package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

func main() {
	bytes, _ := ioutil.ReadFile("data.txt")
	puzzleInput := string(bytes)
	fmt.Println(Answer1(puzzleInput))
	fmt.Println(Answer2(puzzleInput))
}

type valueStruct struct {
	direction string
	amount    int
}

func makeValues(puzzleInput string) []valueStruct {
	lines := strings.Split(string(puzzleInput), "\n")
	values := make([]valueStruct, len(lines))
	for i, line := range lines {
		parts := strings.Split(line, " ")
		values[i].direction = parts[0]
		values[i].amount, _ = strconv.Atoi(parts[1])
	}
	return values
}

func Answer1(puzzleInput string) int {
	values := makeValues(puzzleInput)
	// fmt.Println(values)

	x := 0
	z := 0

	for _, value := range values {
		if value.direction == "forward" {
			x += value.amount
		}
		if value.direction == "down" {
			z += value.amount
		}
		if value.direction == "up" {
			z -= value.amount
		}
	}

	return x * z
}

func Answer2(puzzleInput string) int {
	values := makeValues(puzzleInput)
	// fmt.Println(values)

	x := 0
	z := 0
	aim := 0

	for _, value := range values {
		if value.direction == "down" {
			aim += value.amount
		}
		if value.direction == "up" {
			aim -= value.amount
		}
		if value.direction == "forward" {
			x += value.amount
			z += aim * value.amount
		}

	}

	return x * z
}
