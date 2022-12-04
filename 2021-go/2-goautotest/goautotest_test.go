package main

import (
	"testing"
)

func TestNothing(t *testing.T) {
	got := TestInput()
	want := 1
	if got != want {
		t.Fatalf(`got %v != want %v`, got, want)
	}
}
