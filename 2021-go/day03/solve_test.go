package main

import (
	"testing"
)
    
const puzzleInput string = 
`00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010`
const correctAnswer1 int = 198 
const correctAnswer2 int = 230 

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