import os
import subprocess


def create_framework():
    # Define the YAML parser scripts for each language
    python_parser = '''import sys
import yaml
import signal

# Function to handle the timeout
def handler(signum, frame):
    raise TimeoutError("Operation timed out after 2 minutes")



def parse_yaml(input_file, output_file):
    # Set the timeout handler to trigger after 120 seconds
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(120)  # Set the alarm for 120 seconds (2 minutes)
    try:
        with open(input_file, 'r') as infile:
            data = yaml.safe_load(infile)
        with open(output_file, 'w') as outfile:
            yaml.dump(data, outfile)
    except TimeoutError as e:
        print(e)
    finally:
        # Disable the alarm
        signal.alarm(0)

if __name__ == "__main__":
    if (len(sys.argv) == 3):
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        if input_file and output_file:
            parse_yaml(input_file, output_file)
    else:
        parse_yaml("/Users/a/PycharmProjects/yamlparsers/input.yaml", "output.yaml")

    '''

    ruby_parser = '''require 'yaml'
require 'timeout'


def parse_yaml(input_file, output_file)
    data = nil # Defining the variable in the outer scope
    begin
      # Set a timeout of 5 seconds
      Timeout.timeout(120) do
        data = YAML.load_file(input_file)
      end
    rescue Timeout::Error
      puts "Task timed out!"
      return # Exit the method early if there was a timeout
    end

    if data
    File.open(output_file, 'w') { |file| file.write(data.to_yaml) }
  else
    puts "Failed to load data."
  end
end

if __FILE__ == $0
    input_file = ARGV[0]
    output_file = ARGV[1]
    if input_file.nil? || output_file.nil?
        puts "Please provide input and output file paths."
        exit 1
    end
    parse_yaml(input_file, output_file)
end
    '''

    go_parser = '''package main

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
    '''

    # Define the Dockerfiles for each language
    python_dockerfile = '''FROM python:3.8-slim

WORKDIR /app

COPY parser.py /app/parser.py

RUN pip install pyyaml

ENTRYPOINT ["python", "/app/parser.py"]

    '''

    ruby_dockerfile = '''FROM ruby:2.7-slim

WORKDIR /app

COPY parser.rb /app/parser.rb

ENTRYPOINT ["ruby", "/app/parser.rb"]
    '''

    go_dockerfile = '''FROM golang:1.23.1

WORKDIR /app

COPY parser.go /app/parser.go

RUN go mod init gin

RUN go mod tidy

RUN go get gopkg.in/yaml.v3

ENTRYPOINT ["go", "run", "/app/parser.go"]
    '''

    # Create directory structure
    os.makedirs('yaml_parsers/python', exist_ok=True)
    os.makedirs('yaml_parsers/ruby', exist_ok=True)
    os.makedirs('yaml_parsers/go', exist_ok=True)

    # Write the files for Python
    with open('yaml_parsers/python/parser.py', 'w') as f:
        f.write(python_parser)

    with open('yaml_parsers/python/Dockerfile', 'w') as f:
        f.write(python_dockerfile)

    # Write the files for Ruby
    with open('yaml_parsers/ruby/parser.rb', 'w') as f:
        f.write(ruby_parser)

    with open('yaml_parsers/ruby/Dockerfile', 'w') as f:
        f.write(ruby_dockerfile)

    # Write the files for Go
    with open('yaml_parsers/go/parser.go', 'w') as f:
        f.write(go_parser)

    with open('yaml_parsers/go/Dockerfile', 'w') as f:
        f.write(go_dockerfile)

    print("Docker setup completed.")


# Build the Docker image for all languages
def build_docker_image():
    # Construct the Docker build command for all languages
    build_command_python = [
        "docker", "build", "-t", "python-yaml-parser",
        os.path.join(os.getcwd(), "yaml_parsers/python")
    ]
    build_command_go = [
        "docker", "build", "-t", "go-yaml-parser",
        os.path.join(os.getcwd(), "yaml_parsers/go")
    ]
    build_command_ruby = [
        "docker", "build", "-t", "ruby-yaml-parser",
        os.path.join(os.getcwd(), "yaml_parsers/ruby")
    ]

    # Run the Docker build command for all languages
    result_python = subprocess.run(build_command_python, capture_output=True, text=True)
    result_go = subprocess.run(build_command_go, capture_output=True, text=True)
    result_ruby = subprocess.run(build_command_ruby, capture_output=True, text=True)

    # Output the result of the build
    print(result_python.stdout)
    if result_python.stderr:
        print(f"Error during build: {result_python.stderr}")
    print(result_python.stdout)
    if result_go.stderr:
        print(f"Error during build: {result_go.stderr}")
    print(result_go.stdout)
    if result_ruby.stderr:
        print(f"Error during build: {result_ruby.stderr}")


# 2. Run the Docker container for docker file all languages
def run_docker_container(input_file, output_file):
    # Construct the paths using the current directory
    input_file_path = os.path.join(os.getcwd(), input_file)
    delete_file_python = os.path.join(os.getcwd(), "yaml_parsers/python/input.yaml")
    # delete_file_go = os.path.join(os.getcwd(), "yaml_parsers/go/input.yaml")
    delete_file_ruby = os.path.join(os.getcwd(), "yaml_parsers/ruby/input.yaml")
    volume_path_python = os.path.join(os.getcwd(), "yaml_parsers/python")
    volume_path_go = os.path.join(os.getcwd(), "yaml_parsers/go")
    volume_path_ruby = os.path.join(os.getcwd(), "yaml_parsers/ruby")

    # Docker run command for python
    run_command_python = [
        "docker", "run",
        "-v", f"{input_file_path}:/app/input.yaml",  # Mount input.yaml file
        "-v", f"{volume_path_python}:/app",  # Mount the yaml_parsers/python directory
        "python-yaml-parser",  # Docker image name
        "./input.yaml",  # Input file inside the container
        output_file  # Output file
    ]
    # Docker run command for go
    # -v $(pwd)/yaml_parsers/go/output:/app/output  go-yaml-parser ./input.yaml ./output/output.yaml
    run_command_go = [
        "docker", "run",
        "-v", f"{input_file_path}:/app/input.yaml",  # Mount input.yaml file
        "-v", f"{volume_path_go}/output:/app/output",  # Mount the yaml_parsers/python directory
        "go-yaml-parser",  # Docker image name
        "./input.yaml",  # Input file inside the container
        "./output/" + output_file,
        # output_file  # Output file
    ]
    # Docker run command for ruby
    run_command_ruby = [
        "docker", "run",
        "-v", f"{input_file_path}:/app/input.yaml",  # Mount input.yaml file
        "-v", f"{volume_path_ruby}:/app",  # Mount the yaml_parsers/python directory
        "ruby-yaml-parser",  # Docker image name
        "./input.yaml",  # Input file inside the container
        output_file  # Output file
    ]

    # Run the Docker container for all languages
    result_python = subprocess.run(run_command_python, capture_output=True, text=True)
    result_go = subprocess.run(run_command_go, capture_output=True, text=True)
    result_ruby = subprocess.run(run_command_ruby, capture_output=True, text=True)

    rm_command_python = ["rm", delete_file_python]
    rm_result_python = subprocess.run(rm_command_python, capture_output=True, text=True)
    # rm_command_go = ["rm", delete_file_go]
    # rm_result_go = subprocess.run(rm_command_go, capture_output=True, text=True)
    rm_command_ruby = ["rm", delete_file_ruby]
    rm_result_ruby = subprocess.run(rm_command_ruby, capture_output=True, text=True)
    # Output the result of the run
    print(result_python.stdout)
    if result_python.stderr:
        print(f"Error during run: {result_python.stderr}")
    print(result_go.stdout)
    if result_go.stderr:
        print(f"Error during run: {result_go.stderr}")
    print(result_ruby.stdout)
    if result_ruby.stderr:
        print(f"Error during run: {result_ruby.stderr}")

    print(rm_result_python.stdout)
    if rm_result_python.stderr:
        print(f"Error during file deletion: {rm_result_python.stderr}")
    # print(rm_result_go.stdout)
    # if rm_result_go.stderr:
    #     print(f"Error during file deletion: {rm_result_go.stderr}")
    print(rm_result_ruby.stdout)
    if rm_result_ruby.stderr:
        print(f"Error during file deletion: {rm_result_ruby.stderr}")


# Execute all the functions to create framework and then build docker files and create containers and run them
if __name__ == "__main__":
    # Step 1: Create a framework containing YAML parsers and Docker files for Python, go and Ruby languages
    create_framework()
    # Step 2: Build the Docker image
    build_docker_image()

    # Step 3: Run the Docker container with input.yaml and output.yaml
    run_docker_container("input.yaml", "output.yaml")


