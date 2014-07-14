package config

import (
	"time"
	"io"
	"encoding/json"
	"errors"
)

type KeyValueStore map[string]interface{}


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

	return conf
}

//
// Load configuration file
func (conf *Configuration) load() {

	var raw_data interface{}
	
	// 4kB should be enough
	data_string := make([]byte, 0x1000)
	
	_ , err := conf.Source.Read(data_string)
	
	if err != nil {
		panic(err)
	}

	err = json.Unmarshal(data_string, &raw_data)

	if err != nil {
		panic(err)
	}
	
	conf.data = raw_data.(KeyValueStore)

	conf.deserializeDurations()
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
func (conf *Configuration) Get(key string) (v interface{}, err error) {
	 
	if conf.data[key] != "" {
		return conf.data[key], nil
	}

	return "" , errors.New("Key " + key + " does not exist")
}

//
// Serialization method...
// Prints out Key-Value Pairs
func (conf *Configuration) String() string {
	str := ""

	for k, v := range conf.data {
		str = str + "[" + k + "]" + v.(string) + "\n"
	}

	return str
}

//
// Deserialize the Durations in the configuration data
// Uses the time.ParseDuration method
//
func (conf *Configuration) deserializeDurations() {

	for key, value := range conf.data {
		duration, err := time.ParseDuration(value.(string))

		// If no error was thrown parsing the value,
		// Then it was a duration.
		if err == nil {
			// Replace the string with the time.Duration
			conf.data[key] = duration
		}

	}

}
