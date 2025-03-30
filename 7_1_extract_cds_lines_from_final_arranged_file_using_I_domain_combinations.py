import pandas as pd

# Load the domain combinations from the Input_Combination sheet
input_combinations_path = 'Unique_Domain_Combinations.xlsx'
input_combinations = pd.read_excel(input_combinations_path, sheet_name="Input_Combination")

# Convert domain combinations to a list of sets for exact matching
exact_combinations = [set(row.dropna().tolist()) for _, row in input_combinations.iterrows()]

# Read the HMM scan CDS file
hmm_scan_path = 'query_1_7_final_arranged.txt'
with open(hmm_scan_path, 'r') as file:
    lines = file.readlines()

# Find lines where domain sets match exactly with any of the exact combinations
exact_matches = []
for line in lines:
    parts = line.strip().split('\t')
    if len(parts) > 1:
        domains = set(parts[1:])  # Extract domains as a set
        if domains in exact_combinations:  # Check for exact match
            exact_matches.append(line)

# Save the exact matches to an output file
output_path = 'exact_output_I_1_7.txt'
with open(output_path, 'w') as output_file:
    output_file.writelines(exact_matches)

print(f"Found {len(exact_matches)} matching lines. Results saved to {output_path}.")

