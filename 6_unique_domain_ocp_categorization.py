import pandas as pd

# Load the input Excel file
input_file = 'unique_combinations_ocp.xlsx'  # Replace with the actual input file name
data = pd.read_excel(input_file)

# Initialize three DataFrames for each category
input_combination = pd.DataFrame()
output_combination = pd.DataFrame()
input_output_combination = pd.DataFrame()

# Filter for 'Input_Combination': non-empty 'Input', empty 'Output'
input_combination = data[data['Output'].isna() & data['Input'].notna()][['Input']]

# Filter for 'Output_Combination': non-empty 'Output', empty 'Input'
output_combination = data[data['Input'].isna() & data['Output'].notna()][['Output']]

# Filter for 'Input_Output_Combination': non-empty 'Input' and 'Output'
input_output_combination = data[data['Input'].notna() & data['Output'].notna()][['Input', 'Output']]

# Save to an output Excel file with three sheets
output_file = 'Unique_Domain_Combinations.xlsx'
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    input_combination.to_excel(writer, sheet_name='Input_Combination', index=False)
    output_combination.to_excel(writer, sheet_name='Output_Combination', index=False)
    input_output_combination.to_excel(writer, sheet_name='Input_Output_Combination', index=False)

print(f"Output saved to {output_file}")

