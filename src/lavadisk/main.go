// Main file for lavadisk
//
// Handles the application bootstrapping, and initialization
//
// Forks to the background when ready.
//

package main

import (
	"engine"
)

func main () {

	eng := engine.New()
	eng.Run()
}
