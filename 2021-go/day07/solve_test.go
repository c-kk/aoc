package main

import (
	"testing"
)
    
const puzzleInput string = 
`16,1,2,0,4,2,7,1,2,14`
const correctAnswer1 int = 37 
const correctAnswer2 int = 168

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