import os

# Paths as strings
input_dir = "data/20251201/scion_isd/edgelists"
output_dir = "data/20251201/scion_isd/edgelists_merged"
special_file = os.path.join(input_dir, "20251201.SCION_core_topo.txt")

# Make sure output directory exists
os.makedirs(output_dir, exist_ok=True)

def read_edgelist(path):
    """Read an edgelist file and return a set of edges."""
    with open(path, "r", encoding="latin-1") as f:
        return {line.strip() for line in f if line.strip()}

# Load the special edgelist once
core_edges = read_edgelist(special_file)

# Iterate over all files in input directory
for filename in os.listdir(input_dir):
    full_path = os.path.join(input_dir, filename)
    
    # Skip directories and the special file itself
    if full_path == special_file or not os.path.isfile(full_path):
        continue

    # Read basic edgelist
    basic_edges = read_edgelist(full_path)

    # Merge edges (set union removes duplicates)
    merged_edges = basic_edges | core_edges

    # Output path
    output_path = os.path.join(output_dir, filename)

    # Write merged edgelist
    with open(output_path, "w") as f:
        for edge in sorted(merged_edges):
            f.write(edge + "\n")

    print(f"Merged and saved: {output_path}")
