package main

import (
	"engine"
)

func main () {

	eng := engine.New()
	eng.Logf("[MSG] %s" , "Hello World...")
	
	eng.Logf(eng.Config.String())
}
