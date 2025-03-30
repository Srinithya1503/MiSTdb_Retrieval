import pandas as pd

# Load the Excel file
input_excel_path = 'combining_species_count_hmmscan.xlsx'

# Read the three sheets
species_count_io = pd.read_excel(input_excel_path, sheet_name="IO")
species_count_i = pd.read_excel(input_excel_path, sheet_name="I")
species_count_o = pd.read_excel(input_excel_path, sheet_name="O")

# Combine the Total_Count based on Organism_Name
# Merge all three dataframes, filling missing values with 0
combined_data = pd.merge(species_count_io, species_count_i, on='Organism_Name', how='outer', suffixes=('_IO', '_I'))
combined_data = pd.merge(combined_data, species_count_o, on='Organism_Name', how='outer')

# Fill NaN values in Total_Count columns with 0
combined_data[['Total_Count_IO', 'Total_Count_I', 'Total_Count']] = combined_data[
    ['Total_Count_IO', 'Total_Count_I', 'Total_Count']
].fillna(0)

# Calculate the total count
combined_data['Total_Count_OCP'] = (
    combined_data['Total_Count_IO'] +
    combined_data['Total_Count_I'] +
    combined_data['Total_Count']
)

# Select only necessary columns for the final output
final_data = combined_data[['Organism_Name', 'Total_Count_OCP']]

# Save the aggregated data into a new sheet in the same Excel file
with pd.ExcelWriter(input_excel_path, mode='a', if_sheet_exists='replace') as writer:
    final_data.to_excel(writer, sheet_name="OCP", index=False)

print(f"Aggregated data saved to 'Species_Count_OCP' in {input_excel_path}")

