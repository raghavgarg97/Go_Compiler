package main

import "fmt"

func main() {
	var a [2][2][2][2][2][2][2][2][2][2]int
	a[1][1][1][1][1][1][1][1][1][1] = 1123
	a[1][1][1][1][1][0][1][1][1][1] = 2013
	var c int= a[1][1][1][1][1][1][1][1][1][1]
	var d int = a[1][1][1][1][1][0][1][1][1][1]
	printInt c
	printInt d
}
