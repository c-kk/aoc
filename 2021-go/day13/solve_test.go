package main

import (
	"testing"
)

const puzzleInput string = `6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5`
const correctAnswer1 int = 17
const correctAnswer2 int = 16

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
