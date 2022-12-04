package main

import (
	"testing"
)

const puzzleInput1 string = `7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1`

const puzzleInput2 string = `22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7`

const correctAnswer1 int = 4512
const correctAnswer2 int = 1924

func TestAnswer1(t *testing.T) {
	answer1 := Answer1(puzzleInput1, puzzleInput2)
	if answer1 != correctAnswer1 {
		t.Fatalf("Answer 1: %v is not equal to correct answer %v", answer1, correctAnswer1)
	}
}

func TestAnswer2(t *testing.T) {
	answer2 := Answer2(puzzleInput1, puzzleInput2)
	if answer2 != correctAnswer2 {
		t.Fatalf("Answer 2: %v is not equal to correct answer %v", answer2, correctAnswer2)
	}
}
