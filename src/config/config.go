package config

import (
	"io"
	"encoding/json"
	"errors"
)

type KeyValueStore map[string]string

type JSONMessage struct {
	Key string
	Value string
}

type Configuration struct {
	Source io.Reader
	data KeyValueStore
}

//
// Create a new Configuration Object
//
// source io.Reader  Reader to read source from
func New(source io.Reader) *Configuration {

	// Creat the Configuration
	conf := &Configuration{
		Source: source,
		data: make(KeyValueStore),
	}

	// Try to load the config source
	_ , err := conf.load()

	if err != nil {
		panic(err)
	}

	return conf
}

//
// Load configuration file
func (conf *Configuration) load() (success bool, err error) {
	
	decoder := json.NewDecoder(conf.Source)

	// Iterate over the data and decode.
	for {
		var m JSONMessage

		err := decoder.Decode(&m);

		if err == io.EOF {
			break 
		} else if err != nil {
			panic(err)
		}

		conf.data[m.Key] = m.Value
	
	}

	return true, nil
}

// Set a configuration option
//
// key string Name of option to set
// value interface Value of option to set
func (conf *Configuration) Set(key string, value string) {
	conf.data[key] = value
}

//
//  Get a configuration options
//
// key string Option to getV
func (conf *Configuration) Get(key string) (v string, err error) {
	 
	if conf.data[key] != "" {
		return conf.data[key], nil

	}

	return "" , errors.New("Key " + key + " does not exist")
}

