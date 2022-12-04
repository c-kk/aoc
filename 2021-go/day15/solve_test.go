package main

import (
	"testing"
)

const puzzleInput string = `11199
99199
11199
19999
11111`
const correctAnswer1 int = 40
const correctAnswer2 int = 0

// const puzzleInput string = `1163751742
// 1381373672
// 2136511328
// 3694931569
// 7463417111
// 1319128137
// 1359912421
// 3125421639
// 1293138521
// 2311944581`
// const correctAnswer1 int = 40
// const correctAnswer2 int = 0

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
