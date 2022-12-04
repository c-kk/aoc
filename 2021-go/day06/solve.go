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

func Answer1(puzzleInput string) int {
    lines := strings.Split(puzzleInput, ",")
    fishes := make([]int, 9)

    for _,line := range lines { 
        index,_ := strconv.Atoi(line)
        fishes[index] += 1
    }

    fmt.Println(fishes)

    day := 0
    for day < 80 {
        sum := 0
        for _, count := range fishes { sum += count }
        fmt.Println("day", day, fishes, sum)

        day += 1
        new_fishes := make([]int, 9)

        for index, count := range fishes { 
            if index == 0 {
                new_fishes[6] += count
                new_fishes[8] += count
            } else {
                new_fishes[index-1] += count
            }   
        }
        fishes = new_fishes
    }

    sum := 0
    for _, count := range fishes { sum += count }
    fmt.Println("day", day, fishes, sum)

    return sum
}

func Answer2(puzzleInput string) int {
    lines := strings.Split(puzzleInput, ",")
    fishes := make([]int, 9)

    for _,line := range lines { 
        index,_ := strconv.Atoi(line)
        fishes[index] += 1
    }

    fmt.Println(fishes)

    day := 0
    for day < 256 {
        sum := 0
        for _, count := range fishes { sum += count }
        fmt.Println("day", day, fishes, sum)

        day += 1
        new_fishes := make([]int, 9)

        for index, count := range fishes { 
            if index == 0 {
                new_fishes[6] += count
                new_fishes[8] += count
            } else {
                new_fishes[index-1] += count
            }   
        }
        fishes = new_fishes
    }

    sum := 0
    for _, count := range fishes { sum += count }
    fmt.Println("day", day, fishes, sum)

    return sum
}