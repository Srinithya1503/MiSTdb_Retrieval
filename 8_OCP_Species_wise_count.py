import pandas as pd

# Input file
input_file = "exact_output_O_1_7.txt"

# Output Excel file
output_excel = "species_count_O_1_7.xlsx"

# Temporary storage for processing data
domain_data = []
species_counts = {}

# Process the input file
with open(input_file, 'r') as file:
    for line in file:
        # Extract species name (part before "__peg")
        species = line.split('__peg')[0]

        # Extract protein name (between "[protein=" and "]")
        protein = line.split("[protein=")[-1].split("]")[0]

        # Extract domains (after the last ']')
        domains = line.split(']')[-1].strip()
        domains = ','.join(domains.split())  # Join domains with commas

        # Append to domain data
        domain_data.append([species, protein, domains])

        # Count occurrences of species
        species_counts[species] = species_counts.get(species, 0) + 1

# Prepare domain data as a DataFrame
df_domains = pd.DataFrame(domain_data, columns=["Organism_Name", "Protein_Name", "Domains"])

# Convert species counts to a DataFrame
df_species_counts = pd.DataFrame(list(species_counts.items()), columns=["Organism_name", "Total_Count"])

# Write both DataFrames to a single Excel file with two sheets
with pd.ExcelWriter(output_excel, engine="xlsxwriter") as writer:
    df_domains.to_excel(writer, sheet_name="Domain_Details_O", index=False)
    df_species_counts.to_excel(writer, sheet_name="Species_Counts_O", index=False)

print(f"Excel file with domain details and species counts saved to {output_excel}")


