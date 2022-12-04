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
    lines := strings.Split(puzzleInput, "\n")
    line := lines[0]
    inputs := strings.Split(line, " | ")
    hints := strings.Split(inputs[0], " ")
    toDecode := strings.Split(inputs[1], " ")
    fmt.Println("Hints", hints, "To decode", toDecode)

    positions := make([][]string,7)

    for i := range positions {
        positions[i] = []string{"a","b","c","d","e","f","g"}
    }

    // 1 is the only number with 2 segments
    // The characters in those segments must be in position 2 and 5
    hintWithLength2 := filterByStringLength(hints, 2)[0]
    fmt.Println("Length 2", hintWithLength2)
    positions[2] = []string{}
    positions[5] = []string{}
    for _,rune := range hintWithLength2 {
        char := string(rune)
        for i := range positions {
            positions[i] = removeItemByValue(positions[i], char)
        }
        positions[2] = append(positions[2], char)
        positions[5] = append(positions[5], char)
    }
    fmt.Println("Positions", positions)

    // 7 is the only number with 3 segments
    // The character that is not in the hintWithLength2 must be in position 0
    hintWithLength3 := filterByStringLength(hints, 3)[0]
    fmt.Println("Length 3", hintWithLength3)
    positions[0] = []string{}
    for _,rune := range hintWithLength3 {
        char := string(rune)
        if hasItem(positions[2], char) {
            continue
        }
        for i := range positions {
            positions[i] = removeItemByValue(positions[i], char)
        }
        positions[0] = append(positions[0], char)
    }
    fmt.Println("Positions", positions)


    return 0
}

func filterByStringLength(strings []string, length int) []string {
    filtered := []string{}
    for i := range strings {
        if len(strings[i]) == length {
            filtered = append(filtered, strings[i])
        }
    }
    return filtered
}

func removeItemByValue(strings []string, item string) []string {
    filtered := []string{}
    for _,string := range strings {
        if string != item {
            filtered = append(filtered, string)
        }
    }
    return filtered
}

func hasItem(strings []string, item string) bool {
    for _,string := range strings {
        if string == item {
            return true
        }
    }
    return false
}

// positions := []string {}

// numbers := [][]int {
//     {0,1,2,4,5,6},
//     {2,5},
//     {0,2,3,4,6},
//     {0,2,3,5,6},
//     {1,2,3,5},
//     {0,1,3,5,6},
//     {0,1,3,4,5,6},
//     {0,2,5},
//     {0,1,2,3,4,5,6},
//     {0,1,2,3,5,6},
// }
// fmt.Println(numbers)



// values := strings.Split(lineWithoutDelimiter, " ")

// for _,value := range values {
//     fmt.Println(value)
// }

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
