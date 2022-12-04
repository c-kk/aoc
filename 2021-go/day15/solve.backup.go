package main

import (
	"fmt"
	"io/ioutil"
	"strings"
	"strconv"
)

func main() {
	bytes, _ := ioutil.ReadFile("data.txt")
	puzzleInput := string(bytes)
	fmt.Println(Answer1(puzzleInput))
	fmt.Println(Answer2(puzzleInput))
}

func Answer1(puzzleInput string) int {
	lines := strings.Split(puzzleInput, "\n")
	field := convertStringSliceToIntSlices(lines)
	summed := createEmptyField(field)
	for _, row := range field {
		fmt.Printf("Field  ")
		for _, val := range row {
			fmt.Printf("%02d ", val)
		}
		fmt.Println()
	}
	fmt.Println()

	// summed[0][0] = 0
	// cells := [][]int{}
	// cell := []int{0, 0, 0}
	// cells = append(cells, cell)


	lenf := len(field)

	for i := 0; i < lenf * 2; i++ {
		for j := 0; j <= i; j++ {
			y := j
			x := -j+i
			// fmt.Println(x, y)
			
			if x >= 0 && x < lenf && y >=0 && y < lenf {
				value := summed[y][x]
				// summed[y][x] = value

				if x+1 < lenf {
					left := value + field[y][x+1]
					if left < summed[y][x+1] || summed[y][x+1] == 0 {
						summed[y][x+1] = left
					}
				}

				if y+1 < lenf {
					down := value + field[y+1][x]
					if down < summed[y+1][x] || summed[y+1][x] == 0 {
						summed[y+1][x] = down
					}
				}
				
			} 
		}
	}

	for _, row := range summed {
		fmt.Printf("Summed ")
		for _, val := range row {
			fmt.Printf("%02d ", val)
		}
		fmt.Println()
	}


	lenf2 := len(field[0])
	fmt.Println(lenf, lenf2)

	return summed[lenf-1][lenf-1]
}


func createEmptyField(field [][]int) [][]int {
	yLen := len(field)
	xLen := len(field[0])
	emptyField := make([][]int, yLen)
	for i := range emptyField {
	    emptyField[i] = make([]int, xLen)
	}
	return emptyField
}

// Convert a string slice to int slices
// Example: ["2199943210", "3987894921"] to [[2 1 9 9 9 4 3 2 1 0][3 9 8 7 8 9 4 9 2 1]]
func convertStringSliceToIntSlices(strings []string) [][]int {
	var intSlices [][]int
	for _, str := range strings {
		var intSlice []int
		for _, rune := range str {
			int, _ := strconv.Atoi(string(rune))
			intSlice = append(intSlice, int)
		}
		intSlices = append(intSlices, intSlice)
	}
	return intSlices
}

func Answer2(puzzleInput string) int {
	// lines := strings.Split(puzzleInput, "\n")

	return 0
}
