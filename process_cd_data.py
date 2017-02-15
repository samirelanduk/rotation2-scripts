import sys
print("")

# Get arguments
if len(sys.argv) <= 1:
    print("Please provide a path to the sample data\n")
    sys.exit()
sample_path = sys.argv[1]
if len(sys.argv) <= 2:
    print("Please provide a path to the blank data\n")
    sys.exit()
blank_path = sys.argv[2]
if len(sys.argv) <= 3:
    print("Where should the output .dat be saved?\n")
    sys.exit()
output_path = sys.argv[3]
