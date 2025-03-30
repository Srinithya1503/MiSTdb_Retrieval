import pandas as pd

# Load the Excel file
file_path = 'input_output_domains_ocp_total.xlsx'  # Replace with your Excel file path
df = pd.read_excel(file_path)

# Extract unique combinations of 'input' and 'output'
unique_combinations = df[['Input', 'Output']].drop_duplicates()

# Save the unique combinations to a new Excel file
output_file = 'unique_combinations_ocp.xlsx'
unique_combinations.to_excel(output_file, index=False)

print(f"Unique combinations saved to {output_file}")

