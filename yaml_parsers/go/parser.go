package main
    
import (
    "gopkg.in/yaml.v2"
    "io/ioutil"
    "log"
    "os"
    "fmt"
    "time"
)

func parseYaml(inputFile string, outputFile string, done chan bool) {
    yamlFile, err := ioutil.ReadFile(inputFile)
    if err != nil {
        log.Fatalf("Error reading YAML file: %v", err)
    }

    var data interface{}
    err = yaml.Unmarshal(yamlFile, &data)
    if err != nil {
        log.Fatalf("Error unmarshaling YAML: %v", err)
    }

    outputYaml, err := yaml.Marshal(&data)
    if err != nil {
        log.Fatalf("Error marshaling YAML: %v", err)
    }

    err = ioutil.WriteFile(outputFile, outputYaml, 0644)
    if err != nil {
        log.Fatalf("Error writing YAML file: %v", err)
    }
    done <- true // Signal that the task is done
}

func main() {
    if len(os.Args) < 3 {
        log.Fatalf("Usage: %s <input_yaml> <output_yaml>", os.Args[0])
    }

    done := make(chan bool, 1)

    // Start the YAML parsing in a separate goroutine
    go parseYaml(os.Args[1], os.Args[2], done)

    // Create a timeout for 2 minutes (120 seconds)
    timeout := time.After(120 * time.Second)

    select {
    case <-done:
        // Task finished successfully
        fmt.Println("YAML file processed successfully.")
    case <-timeout:
        // Task did not finish within 2 minutes
        fmt.Println("YAML file processing timed out after 2 minutes!")
    }
}
    