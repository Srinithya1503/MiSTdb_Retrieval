import json
import csv
import os

# Directory containing the input JSON files
input_directory = "/home/iith/bio/srinithya/phylum_actinomycetota/genomic_data_2024/assembly_statistics_scripts_output_/hmmscan/STP_Domain_sorting/OCS_domain_sorting/ocp_rest_api_retrieval/ocp_outputs_rest_api/ocp_output_alphabetical_cds_693/ocp_output_98_1"
output_file = "/home/iith/bio/srinithya/phylum_actinomycetota/genomic_data_2024/assembly_statistics_scripts_output_/hmmscan/STP_Domain_sorting/OCS_domain_sorting/ocp_rest_api_retrieval/ocp_outputs_rest_api/ocp_cds_wise_count/output_ocp_98_1.tsv"

# Initialize a list to store results
results = []

# Process each JSON file in the directory
for filename in os.listdir(input_directory):
    if filename.endswith("_ocp.json"):  # Only process JSON files with the specified suffix
        input_file = os.path.join(input_directory, filename)

        # Read the JSON data
        with open(input_file, "r") as f:
            data = json.load(f)

        # Dictionary to store combinations and their counts for this file
        combinations = {}

        # Process each entry in the JSON data
        for entry in data:
            inputs = entry.get("inputs", [])
            outputs = entry.get("outputs", [])
            counts = entry.get("counts", {})

            # Iterate over all combinations of inputs and outputs
            for inp in inputs if inputs else [None]:  # Handle cases with no input
                for out in outputs if outputs else [None]:  # Handle cases with no output
                    key = (inp, out)
                    combinations[key] = combinations.get(key, 0) + 1

        # Add the results to the overall list
        file_name = filename.replace("_ocp.json", "")
        for (inp, out), count in combinations.items():
            results.append([file_name, inp if inp else "None", out if out else "None", count])

# Write all results to a single TSV file
with open(output_file, "w", newline="") as tsv_file:
    writer = csv.writer(tsv_file, delimiter="\t")
    writer.writerow(["File Name", "Input", "Output", "Count"])
    writer.writerows(results)

print(f"Output saved to {output_file}")
