package main

import (
	"fmt"
	"io/ioutil"
	"math"
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
    // fmt.Println(sums)
    gamma := 0
    epsilon := 0

    for j, sum := range sums {
        position := len(sums) - j - 1

        if sum > len(lines)/2 {
            gamma += int(math.Exp2(float64(position)))
            // fmt.Println("gamma", gamma)
        } else {
            epsilon += int(math.Exp2(float64(position)))
            // fmt.Println("epsilon", epsilon)
        }
    }

    return gamma * epsilon
}

func Answer2(puzzleInput string) int {
    return 0
}
