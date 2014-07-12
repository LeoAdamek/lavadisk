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

	eng := &Engine {
		Stdout: os.Stdout,
		Stderr: os.Stderr,
		Stdin: os.Stdin,
		Logging: true,
	}

	// Load the config_file argument
	config_file_location := flag.String("config-file" , "config.json", "Configuration File Location")
	println(config_file_location)
	eng.Config = *config.New(os.Stdin)
	
	return eng
}



//
// Log something (with formatting)
// 
func (eng *Engine) Logf(format string, args ...interface{}) (n int, err error) {
	
	// Just succeed if there's no logging
	if !eng.Logging {
		return 0, nil
	}

	return fmt.Fprintf(eng.Stderr, format, args...)
}
