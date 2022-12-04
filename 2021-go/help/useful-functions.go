package main

import (
	"fmt"
	"strconv"
	"time"
)

// Convert a string slice to int slices
// Example: ["2199943210", "3987894921"] to [[2 1 9 9 9 4 3 2 1 0][3 9 8 7 8 9 4 9 2 1]]
// Used in: 2021 day 9 for an underwater depth map
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

// Create 3-dimensional slice (or more than 3)
// Source: https://stackoverflow.com/questions/13619633/create-3-dimensional-slice-or-more-than-3/13619634
// Used in: none yet
func createWorld() [][][]int {
	var xs, ys, zs = 5, 6, 7
	var world = make([][][]int, xs)
	for x := 0; x < xs; x++ {
		world[x] = make([][]int, ys)
		for y := 0; y < ys; y++ {
			world[x][y] = make([]int, zs)
			for z := 0; z < zs; z++ {
				world[x][y][z] = (x+1)*100 + (y+1)*10 + (z+1)*1
			}
		}
	}
	return world
}

// Get current date and time in various formats
// Source: https://www.golangprograms.com/get-current-date-and-time-in-various-format-in-golang.html
// Used in: goautotest
func printDateAndTime() {
	currentTime := time.Now()
	fmt.Println("Current Time in String: ", currentTime.String())
	fmt.Println("MM-DD-YYYY : ", currentTime.Format("01-02-2006"))
	fmt.Println("YYYY-MM-DD : ", currentTime.Format("2006-01-02"))
	fmt.Println("YYYY.MM.DD : ", currentTime.Format("2006.01.02 15:04:05"))
	fmt.Println("YYYY#MM#DD {Special Character} : ", currentTime.Format("2006#01#02"))
	fmt.Println("YYYY-MM-DD hh:mm:ss : ", currentTime.Format("2006-01-02 15:04:05"))
	fmt.Println("Time with MicroSeconds: ", currentTime.Format("2006-01-02 15:04:05.000000"))
	fmt.Println("Time with NanoSeconds: ", currentTime.Format("2006-01-02 15:04:05.000000000"))
	fmt.Println("ShortNum Month : ", currentTime.Format("2006-1-02"))
	fmt.Println("LongMonth : ", currentTime.Format("2006-January-02"))
	fmt.Println("ShortMonth : ", currentTime.Format("2006-Jan-02"))
	fmt.Println("ShortYear : ", currentTime.Format("06-Jan-02"))
	fmt.Println("LongWeekDay : ", currentTime.Format("2006-01-02 15:04:05 Monday"))
	fmt.Println("ShortWeek Day : ", currentTime.Format("2006-01-02 Mon"))
	fmt.Println("ShortDay : ", currentTime.Format("Mon 2006-01-2"))
	fmt.Println("Short Hour Minute Second: ", currentTime.Format("2006-01-02 3:4:5"))
	fmt.Println("Short Hour Minute Second: ", currentTime.Format("2006-01-02 3:4:5 PM"))
	fmt.Println("Short Hour Minute Second: ", currentTime.Format("2006-01-02 3:4:5 pm"))
}
