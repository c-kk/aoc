package main

import (
	"fmt"
	"io/ioutil"
	"sort"
	"strings"
)

func main() {
	bytes, _ := ioutil.ReadFile("data.txt")
	puzzleInput := string(bytes)
	fmt.Println(Answer1(puzzleInput))
	fmt.Println(Answer2(puzzleInput))
}

func Answer1(puzzleInput string) int {
	stringLines := strings.Split(puzzleInput, "\n")
	lines := convertStringSliceToStringSlices(stringLines)
	printSlice(lines)

	errorScore := 0

	for index, line := range lines {
		lineIsCorrupted := false
		foundOpeners := []string{}
		currentOpener := ""
		expectedCloser := ""
		for charIndex, char := range line {
			if char == "(" || char == "[" || char == "{" || char == "<" {
				foundOpeners = append(foundOpeners, char)
			}

			if char == ")" || char == "]" || char == "}" || char == ">" {
				currentOpenerIndex := len(foundOpeners) - 1
				currentOpener = foundOpeners[currentOpenerIndex]
				foundOpeners = foundOpeners[:currentOpenerIndex]

				if currentOpener == "(" {
					expectedCloser = ")"
				}
				if currentOpener == "[" {
					expectedCloser = "]"
				}
				if currentOpener == "{" {
					expectedCloser = "}"
				}
				if currentOpener == "<" {
					expectedCloser = ">"
				}
				if char != expectedCloser {
					lineIsCorrupted = true
				}
			}

			if lineIsCorrupted {
				fmt.Printf("%v - Expected %v, but found %v instead on index %v\n", stringLines[index], expectedCloser, char, charIndex)

				if char == ")" {
					errorScore += 3
				}
				if char == "]" {
					errorScore += 57
				}
				if char == "}" {
					errorScore += 1197
				}
				if char == ">" {
					errorScore += 25137
				}

				break
			}
		}
	}

	return errorScore
}

func Answer2(puzzleInput string) int {
	stringLines := strings.Split(puzzleInput, "\n")
	lines := convertStringSliceToStringSlices(stringLines)
	// printSlice(lines)

	completionScores := []int{}

	for _, line := range lines {
		lineIsCorrupted := false
		foundOpeners := []string{}
		currentOpener := ""
		expectedCloser := ""
		for _, char := range line {
			if char == "(" || char == "[" || char == "{" || char == "<" {
				foundOpeners = append(foundOpeners, char)
			}

			if char == ")" || char == "]" || char == "}" || char == ">" {
				currentOpenerIndex := len(foundOpeners) - 1
				currentOpener = foundOpeners[currentOpenerIndex]
				foundOpeners = foundOpeners[:currentOpenerIndex]

				if currentOpener == "(" {
					expectedCloser = ")"
				}
				if currentOpener == "[" {
					expectedCloser = "]"
				}
				if currentOpener == "{" {
					expectedCloser = "}"
				}
				if currentOpener == "<" {
					expectedCloser = ">"
				}
				if char != expectedCloser {
					lineIsCorrupted = true
				}
			}

			if lineIsCorrupted {
				break
			}
		}
		if !lineIsCorrupted {
			completionScore := 0
			foundOpenersReversed := reverse(foundOpeners)
			for _, opener := range foundOpenersReversed {
				if opener == "(" {
					completionScore *= 5
					completionScore += 1
				}
				if opener == "[" {
					completionScore *= 5
					completionScore += 2
				}
				if opener == "{" {
					completionScore *= 5
					completionScore += 3
				}
				if opener == "<" {
					completionScore *= 5
					completionScore += 4
				}
			}
			// fmt.Println(line)
			fmt.Println("Completion score", completionScore)
			completionScores = append(completionScores, completionScore)
		}
	}

	sort.Ints(completionScores)
	middleScore := completionScores[(len(completionScores))/2]

	return middleScore
}

// Convert a string slice to string slices
// Example: ["abc", "def"] to [["a" "b" "c"]["d" "e" "f"]]
func convertStringSliceToStringSlices(stringSliceInput []string) [][]string {
	var stringSlices [][]string
	for _, str := range stringSliceInput {
		var stringSliceOutput []string
		for _, rune := range str {
			char := string(rune)
			stringSliceOutput = append(stringSliceOutput, char)
		}
		stringSlices = append(stringSlices, stringSliceOutput)
	}
	return stringSlices
}

// Print a slice with one item per line
// Instruction: adjust the type of slice to match the actual type
func printSlice(slice [][]string) {
	for _, item := range slice {
		fmt.Println(item)
	}
}

// string was interface{}
// https://stackoverflow.com/questions/28058278/how-do-i-reverse-a-slice-in-go
// https://github.com/golang/go/wiki/SliceTricks#reversing
func reverse(s []string) []string {
	a := make([]string, len(s))
	copy(a, s)

	for i := len(a)/2 - 1; i >= 0; i-- {
		opp := len(a) - 1 - i
		a[i], a[opp] = a[opp], a[i]
	}

	return a
}
