import os
import pandas as pd

# File and directory paths
tsv_file = "ocp_693_filename_change.tsv"
ocp_dir = "/home/iith/bio/srinithya/phylum_actinomycetota/genomic_data_2024/assembly_statistics_scripts_output_/hmmscan/STP_Domain_sorting/OCS_domain_sorting/ocp_rest_api_retrieval/ocp_outputs_rest_api/ocp_output_693"

# Read the TSV file into a DataFrame
df = pd.read_csv(tsv_file, sep="\t")  # Adjust delimiter if not tab-separated
mapping = dict(zip(df['Assembly_Accession'], df['Organism_Name']))

# Iterate over files in the directory
for filename in os.listdir(ocp_dir):
    if filename.endswith("_ocp.json"):
        # Extract the Assembly Accession number from the filename
        accession = filename.split("_ocp.json")[0]
        if accession in mapping:
            # Get the corresponding organism name
            organism_name = mapping[accession]
            # Construct the new filename
            new_filename = f"{organism_name}_ocp.json"
            # Rename the file
            old_path = os.path.join(ocp_dir, filename)
            new_path = os.path.join(ocp_dir, new_filename)
            os.rename(old_path, new_path)
            print(f"Renamed: {old_path} -> {new_path}")
