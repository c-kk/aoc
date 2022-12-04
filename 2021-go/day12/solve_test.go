package main

import (
	"testing"
)

const puzzleInput string = `start-A
start-b
A-c
A-b
b-d
A-end
b-end`
const correctAnswer1 int = 10
const correctAnswer2 int = 36

// const puzzleInput string = `dc-end
// HN-start
// start-kj
// dc-start
// dc-HN
// LN-dc
// HN-end
// kj-sa
// kj-HN
// kj-dc`
// const correctAnswer1 int = 19
// const correctAnswer2 int = 103

// const puzzleInput string = `fs-end
// he-DX
// fs-he
// start-DX
// pj-DX
// end-zg
// zg-sl
// zg-pj
// pj-he
// RW-he
// fs-DX
// pj-RW
// zg-RW
// start-pj
// he-WI
// zg-he
// pj-fs
// start-RW`
// const correctAnswer1 int = 226
// const correctAnswer2 int = 3509

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
