package main

import (
	"fmt"
	"io/ioutil"
	"strconv"
	"strings"
)

func main() {
	bytes1, _ := ioutil.ReadFile("data1.txt")
	puzzleInput1 := string(bytes1)
	bytes2, _ := ioutil.ReadFile("data2.txt")
	puzzleInput2 := string(bytes2)

	fmt.Println(Answer1(puzzleInput1, puzzleInput2))
	fmt.Println(Answer2(puzzleInput1, puzzleInput2))
}

func Answer1(puzzleInput1 string, puzzleInput2 string) int {
	draws := createDraws(puzzleInput1)
	boards := createBoards(puzzleInput2)
	boards, winningBoardIndex, winningDraw := drawNumbers(draws, boards)
	sumWinningBoard := sumNumbersLeftOnBoard(boards[winningBoardIndex])
	answer := winningDraw * sumWinningBoard
	return answer
}

func Answer2(puzzleInput1 string, puzzleInput2 string) int {
	draws := createDraws(puzzleInput1)
	boards := createBoards(puzzleInput2)
	winningBoard, winningDraw := drawUntilOneBoardIsLeft(draws, boards)
	sumWinningBoard := sumNumbersLeftOnBoard(winningBoard)
	answer := winningDraw * sumWinningBoard
	return answer
}

type Row struct {
	numbers []int
}

type Board struct {
	rows []Row
}

func createDraws(puzzleInput1 string) []int {
	numStrings := strings.Split(string(puzzleInput1), ",")
	return convertToInts(numStrings)
}

func createBoards(puzzleInput2 string) []Board {
	var boards []Board
	boardsStrings := strings.Split(string(puzzleInput2), "\n\n")
	for _, boardStrings := range boardsStrings {
		var board Board

		// Add horizontal rows
		rowStrings := strings.Split(string(boardStrings), "\n")
		for _, rowString := range rowStrings {
			rowInts := convertToInts(strings.Fields(rowString))
			row := Row{numbers: rowInts}
			board.rows = append(board.rows, row)
		}

		// Add vertical rows
		for i := 0; i <= 4; i++ {
			row := Row{}
			for j := 0; j <= 4; j++ {
				row.numbers = append(row.numbers, board.rows[j].numbers[i])
			}
			board.rows = append(board.rows, row)
		}
		boards = append(boards, board)
	}
	return boards
}

func drawNumbers(draws []int, boards []Board) ([]Board, int, int) {
	for _, draw := range draws {
		//fmt.Println(i, draw)
		for j, board := range boards {
			for k, row := range board.rows {
				for l, number := range row.numbers {
					if draw == number {
						numbers := row.numbers
						numbers[l] = numbers[len(numbers)-1]
						boards[j].rows[k].numbers = numbers[:len(numbers)-1]
						if len(boards[j].rows[k].numbers) == 0 {
							return boards, j, draw
						}
					}
				}
			}
		}
	}
	return make([]Board, 0), 0, 0
}

func sumNumbersLeftOnBoard(board Board) int {
	sum := 0
	for i := 0; i <= 4; i++ {
		for _, number := range board.rows[i].numbers {
			sum += number
		}
	}
	return sum
}

func drawUntilOneBoardIsLeft(draws []int, boards []Board) (Board, int) {
	for {
		boards, winningBoardIndex, winningDraw := drawNumbers(draws, boards)
		winningBoard := boards[winningBoardIndex]
		boards[winningBoardIndex] = Board{}

		allDone := true
		for _, board := range boards {
			if len(board.rows) > 0 {
				allDone = false
			}
		}

		if allDone {
			return winningBoard, winningDraw
		}
	}
}

func convertToInts(numStrings []string) []int {
	var numInts []int
	for _, numString := range numStrings {
		numInt, _ := strconv.Atoi(numString)
		numInts = append(numInts, numInt)
	}
	return numInts
}
