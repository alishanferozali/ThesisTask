import sys
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
    
    