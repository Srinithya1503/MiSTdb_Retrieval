import pandas as pd

# Define the input and output file paths
input_file =  r"taxonomy_stp_distribution_sheet.xlsx"
output_file = r"stp_count_family_wise.xlsx"

# Read the input Excel file
data = pd.read_excel(input_file)

# Select the range of columns to analyze (5th to 18th)
start_col = 4  # Zero-indexed, so 5th column is index 4
end_col = 18   # Zero-indexed, end is exclusive

# Group by 'family' column (2nd column, index 1) and count non-NaN values
counts = data.iloc[:, start_col:end_col].notna().groupby(data.iloc[:, 1]).sum()

# Rename the columns as count_1, count_2, ..., count_14
counts.columns = [f"count_{i+1}" for i in range(counts.shape[1])]

# Reset the index to have 'family' as a column
counts.reset_index(inplace=True)

# Save the output to an Excel file
counts.to_excel(output_file, index=False)

print(f"Output saved to: {output_file}")

