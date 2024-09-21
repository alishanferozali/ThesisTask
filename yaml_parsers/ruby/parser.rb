require 'yaml'
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
    