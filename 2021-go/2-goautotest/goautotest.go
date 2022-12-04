// Goal
// Automatically run 'go test' when a file in the current directory is changed

// Inspiration
// https://medium.com/@skdomino/watch-this-file-watching-in-go-5b5a247cf71f
// https://github.com/fsnotify/fsnotify
// https://github.com/eiannone/keyboard

package main

import (
	"fmt"
	"os"
	"os/exec"
	"time"

	"github.com/eiannone/keyboard"
	"github.com/fsnotify/fsnotify"
)

func main() {
	keysEvents, _ := keyboard.GetKeys(10)
	defer func() {
		_ = keyboard.Close()
	}()

	fmt.Println("goautotest runs 'go test' on a file change in current dir. Press ESC to quit")
	runGoTest()

	// Create new file watcher
	watcher, err := fsnotify.NewWatcher()
	if err != nil {
		fmt.Println("ERROR", err)
	}

	defer watcher.Close()
	done := make(chan bool)

	oldTime := time.Now()
	go func() {
		for {
			select {
			case event := <-watcher.Events:
				// Measure the time difference between two testruns
				// Only allow a new testrun every couple of seconds
				newTime := time.Now()
				diff := newTime.Sub(oldTime)
				if diff < 2*time.Second {
					continue
				}
				oldTime = newTime
				fmt.Println(newTime.Format("15:04:05"), event.Name, "changed")
				runGoTest()

			case keyEvent := <-keysEvents:
				// fmt.Printf("You pressed: rune %q, key %X\r\n", keyEvent.Rune, keyEvent.Key)
				if keyEvent.Key == keyboard.KeyEsc || keyEvent.Key == keyboard.KeyCtrlZ {
					keyboard.Close()
					os.Exit(1)
				}
			}
		}
	}()

	watcher.Add("./")
	<-done
}

func runGoTest() {
	out, _ := exec.Command("go", "test").Output()
	fmt.Printf("%s", out)
}

func TestInput() int {
	return 1
}
