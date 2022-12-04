package main

import (
	"fmt"
	"io/ioutil"
	"strings"
    // "strconv"
)

func main() {
    bytes, _ := ioutil.ReadFile("data.txt")
    puzzleInput := string(bytes)
    fmt.Println(Answer1(puzzleInput))
    fmt.Println(Answer2(puzzleInput))
}

func Answer1(puzzleInput string) int {
    lines := strings.Split(puzzleInput, "\n")
    // fmt.Println(lines)

    // var signalPatterns []string
    var outputValues []string
    
    for _,line := range lines {
        inputs := strings.Split(line, " | ")
        // fmt.Println("Line", line, "Inputs", inputs[1])
        for _,input := range strings.Split(inputs[1], " ") {
            outputValues = append(outputValues, input)
            // fmt.Println(input)
        }
    }

    // 1 => 2
    // 4 => 4
    // 7 => 3
    // 8 => 7
    count1478 := 0
    for _,outputValue := range outputValues {
        length := len(outputValue)
        if length == 2 || length == 4 || length == 3 || length == 7 {
            count1478 += 1
            // fmt.Println(count1478, outputValue)    
        }
        
    }

    return count1478
}

func Answer2(puzzleInput string) int {
    numbers := [][]int {
        {0,1,2,4,5,6},
        {2,5},
        {0,2,3,4,6},
        {0,2,3,5,6},
        {1,2,3,5},
        {0,1,3,5,6},
        {0,1,3,4,5,6},
        {0,2,5},
        {0,1,2,3,4,5,6},
        {0,1,2,3,5,6},
    }
    fmt.Println(numbers)

    lines := strings.Split(puzzleInput, "\n")
    line := lines[0]
    lineWithoutDelimiter := strings.ReplaceAll(line, " | ", "")
    values := strings.Split(lineWithoutDelimiter, " ")

    for _,value := range values {
        fmt.Println(value)
    }

    return 0
}

// fmt.Println(lines)
// numbers2 := [][]string {
//     {"a","b","c","e","f","g"},
//     {"c","f"},
//     {"a","c","d","e","g"},
//     {"a","c","d","f","g"},
//     {"b","c","d","f"},
//     {"a","b","d","f","g"},
//     {"a","b","d","f","g", "e"},
//     {"a","c","f"},
//     {"a","b","c","d","e","f","g"},
//     {"a","b","c","d","f","g"},
// }
