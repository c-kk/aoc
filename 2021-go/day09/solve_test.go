package main

import (
	"testing"
)

const puzzleInput string = `2199943210
3987894921
9856789892
8767896789
9899965678`
const correctAnswer1 int = 15
const correctAnswer2 int = 0

func TestAnswer1(t *testing.T) {
	answer1 := Answer1(puzzleInput)
	if answer1 != correctAnswer1 {
		t.Fatalf("Answer 1: %v is not equal to correct answer %v", answer1, correctAnswer1)
	}
}

func TestAnswer2(t *testing.T) {
	answer2 := Answer2(puzzleInput)
	if answer2 != correctAnswer2 {
		t.Fatalf("Answer 2: %v is not equal to correct answer %v", answer2, correctAnswer2)
	}
}
