package main

import (
	"testing"
)
    
const puzzleInput string = 
`0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2`
const correctAnswer1 int = 5 
const correctAnswer2 int = 12 

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