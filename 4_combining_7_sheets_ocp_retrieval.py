import pandas as pd

# Path to the Excel workbook
file_path = 'ocp_cds_wise_count.xlsx'  # Replace with your workbook's path

# Load the workbook
excel_data = pd.ExcelFile(file_path)

# Initialize an empty DataFrame to hold the combined data
combined_data = pd.DataFrame()

# Loop through all sheets and extract all four columns
for sheet_name in excel_data.sheet_names:
    # Read the sheet into a DataFrame
    sheet_data = excel_data.parse(sheet_name)
    
    # Select all four columns: 'Organism_Name' (1st), 'Input' (2nd), 'Output' (3rd), 'Count' (4th)
    selected_data = sheet_data.iloc[:, [0, 1, 2, 3]]  # Columns are 0-indexed
    
    # Append the data to the combined DataFrame
    combined_data = pd.concat([combined_data, selected_data], ignore_index=True)

# Save the combined data to a new sheet
output_file = 'combined_ocp_cds_wise_count.xlsx'
combined_data.to_excel(output_file, index=False, header=['Organism_Name', 'Input', 'Output', 'Count'])

print(f"Combined data saved to {output_file}")

