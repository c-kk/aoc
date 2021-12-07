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
    positions := convertToInts(lines)

    // Start at position 0
    // Keep increasing the position with 1
    // Calculate the needed fuel at each step
    // If more fuel is needed than in the previous position,
    // the previous position is the optimal position with lowest amount of fuel needed 
    targetPosition := 0
    previousFuel := 0

    for {
        fuel := calculateNeededFuel(positions, targetPosition)
        fmt.Println("Target position:", targetPosition, "Fuel needed:", fuel)
        if fuel > previousFuel && previousFuel != 0 {
            break
        }
        targetPosition += 1
        previousFuel = fuel    
    }

    return previousFuel
}

func Answer2(puzzleInput string) int {
    lines := strings.Split(puzzleInput, ",")
    positions := convertToInts(lines)

    // Same solution as for answer 1
    // The only difference is calculating the needed fuel with an increasing rate
    targetPosition := 0
    previousFuel := 0

    for {
        fuel := calculateNeededFuelAtIncreasingRate(positions, targetPosition)
        fmt.Println("Target position:", targetPosition, "Fuel needed:", fuel)
        if fuel > previousFuel && previousFuel != 0 {
            break
        }
        targetPosition += 1
        previousFuel = fuel    
    }

    return previousFuel
}

func calculateNeededFuel(positions []int, targetPosition int) int {
    sum := 0
    for _,position := range positions {
        fuelNeeded := abs(targetPosition - position)
        sum += fuelNeeded
    }
    return sum
}

func calculateNeededFuelAtIncreasingRate(positions []int, targetPosition int) int {
    sum := 0
    for _,position := range positions {
        fuelNeeded := 0
        distance := abs(targetPosition - position)
        for d := 1; d <= distance; d++ {
            fuelNeeded += d
        }
        sum += fuelNeeded
    }
    return sum
}

func convertToInts(numStrings []string) []int {
    var numInts []int 
    for _, numString := range numStrings {
        numInt,_ := strconv.Atoi(numString)
        numInts = append(numInts, numInt)
    }
    return numInts
}

func abs(x int) int {
    if x < 0 {
        return -x
    } else {
        return x
    }
}