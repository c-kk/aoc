# Open a file
lines = open(f"data{sys.argv[1]}.txt").read().split('\n')

# Split by * and +, () = keep delimiters
splitted = re.split("(\*|\+)", line)

# Print list line by line
print("\n".join(l))

# Alternatives
import yaml
print(yaml.dump(rules))

import json
print(json.dumps(rules, indent = 4))

# Print dict line by line
for key, value in d.items():
	print(key, value)