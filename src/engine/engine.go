//
// Lavadisk Engine
//
// Naievely based on the "engine" from Docker
// But a bit simpler...

package engine

import (
	"io"
	"fmt"
	"os"
	"flag"
	"config"
	"time"
	"os/signal"
)

//
// Installer is an interface for objects which can
// register event handlers for application extension
type Installer interface {
	Install(*Engine) error
}

//
// The engine is the main daemon
// It acts as the platform on which commands are run
// Handles Logging and IO operations too.
type Engine struct {
	Stdout	 io.Writer	// Writer for Stdout
	Stderr	 io.Writer	// Writer for Stderr
	Stdin	 io.Reader	// Reader for Stdin
	Logging	 bool		// Enable Loggin
	Config   config.Configuration	// Configuration
}

//
// Engine Constructor
//
func New() *Engine {

	eng := &Engine{
		Stdout: os.Stdout,
		Stderr: os.Stderr,
		Stdin: os.Stdin,
		Logging: true,
	}

	// Load the config_file argument
	config_file , err := os.Open(*flag.String("config-file" , "config.json", "Configuration File Location"))

	if err != nil {
		panic(err)
	}
	
	eng.Config = *config.New(config_file)
	
	return eng
}

//
// Run
// Runs a main loop at a pre-defined tick-rate
// The loop will be paused for (1/tick-rate) seconds.
// A separate handler for OS Signals is created to handle interruption.
func (eng *Engine) Run() {

	// Spawn a goroutine to handle the OS signal for exit
	go eng.waitForExit()

	// Cerate a ticket to run at the specified tick rate
	d, _ := time.ParseDuration("1s")
	
	ticker := time.NewTicker(d)

	for {
		// Wait for a tick
		tick := <- ticker.C

		// Do a thing
		eng.Logf("Current Time: %s" , time.Now())
		eng.Logf("Tick: %s", tick)
	}
}



//
// Wait for a condition to terminate execution
// 
func (eng *Engine) waitForExit() {
	
	signal_channel := make(chan os.Signal , 1)
	signal.Notify(signal_channel, os.Interrupt)
	
	for {
		
		s := <- signal_channel
		
		if s == os.Interrupt {
			eng.Logf("Interrupted. Exiting")
			os.Exit(0)
		}

	}
	
}


//
// Log something (with formatting)
//
// format string Log format -- Without placeholders can be a constant string
// args ...interface{} Things to use
// 
func (eng *Engine) Logf(format string, args ...interface{}) (n int, err error) {
	
	// Just succeed if there's no logging
	if !eng.Logging {
		return 0, nil
	}

	return fmt.Fprintf(eng.Stderr, format + "\n" , args...)
}
