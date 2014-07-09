// Main file for lavadisk
//
// Handles the application bootstrapping, and initialization
//
// Forks to the background when ready.
//

package main

import (
	"os"
	"os/signal"
)


var signal_channel = make(chan os.Signal, 1)

func main () {

	signal.Notify(signal_channel, os.Interrupt, os.Kill)
	
	// Handle the signals
	handleSignal()



}

func handleSignal ( ) {
	i := 0

	for i < 2 {
		// Wait for signal
		sig := <- signal_channel

		// Handle the signal
		if sig == os.Interrupt {
			if i == 0 {
				println("Press Ctrl+C again to terminate.")
			}
			i++
		}
	}
}

