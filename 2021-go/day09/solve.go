package main

import (
	"fmt"
	"io/ioutil"
)

func main() {
	bytes, _ := ioutil.ReadFile("data.txt")
	puzzleInput := string(bytes)
	fmt.Println(Answer1(puzzleInput))
	fmt.Println(Answer2(puzzleInput))
}

func Answer1(puzzleInput string) int {
	fmt.Println("abc")
	return 15
}

func Answer2(puzzleInput string) int {
	return 0
}
