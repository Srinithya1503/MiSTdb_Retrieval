import http.client
import json
import os

# Input and output files
accessions_file = "accessions.txt"  # File containing accession numbers (one per line)
output_dir = "ocp_output_99_7_28"          # Directory to save filtered outputs
error_log = "error_log_7_28.txt"         # File to log errors

# Pagination settings
items_per_page = 1  # Set how many items you want per page
max_pages = 75        # Set the maximum number of pages to retrieve

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Read accessions from the file
with open(accessions_file, "r") as f:
    accessions = [line.strip() for line in f if line.strip()]

# API connection setup
conn = http.client.HTTPSConnection("mib-jouline-db.asc.ohio-state.edu")

# Initialize counters for tracking progress
total_accessions = len(accessions)
processed_accessions = 0
remaining_accessions = total_accessions
successful_retrievals = 0

# Process each accession
for accession in accessions:
    print(f"Processing accession: {accession}")
    endpoint = f"/v1/genomes/{accession}/signal-genes"
   
    # Initialize pagination variables
    page = 1
    total_results_retrieved = 0
    all_filtered_data = []

    while page <= max_pages:
        # Add pagination parameters to the request URL
        pagination_params = f"?limit={items_per_page}&page={page}"
        full_endpoint = endpoint + pagination_params

        try:
            # Send GET request with pagination
            conn.request("GET", full_endpoint)
            res = conn.getresponse()

            # Handle non-200 responses
            if res.status != 200:
                error_message = f"Error for {accession}: {res.status} {res.reason}\n"
                print(error_message)
                with open(error_log, "a") as error_file:
                    error_file.write(error_message)
                break  # Stop fetching further pages for this accession

            # Read and decode the response
            data = res.read()
            decoded_data = json.loads(data.decode("utf-8"))

            # Filter for entries where 'ranks' contains 'ocp'
            filtered_data = [gene for gene in decoded_data if "ocp" in gene.get("ranks", [])]
            all_filtered_data.extend(filtered_data)  # Add to the list of all results retrieved

            total_results_retrieved += len(filtered_data)
            print(f"Page {page} retrieved. {len(filtered_data)} OCP results found.")

            # If less than the expected number of items, we may have reached the end of data
            if len(decoded_data) < items_per_page:
                break  # Exit loop if we have reached the end

            # Move to the next page
            page += 1

        except Exception as e:
            # Handle unexpected errors
            error_message = f"Exception for {accession} on page {page}: {str(e)}\n"
            print(error_message)
            with open(error_log, "a") as error_file:
                error_file.write(error_message)
            break  # Stop on error

    # Save filtered data to a file
    if all_filtered_data:
        output_file = os.path.join(output_dir, f"{accession}_ocp.json")
        with open(output_file, "w") as f:
            json.dump(all_filtered_data, f, indent=2)
        print(f"Saved OCP data for {accession} to {output_file}")
        successful_retrievals += 1
    else:
        print(f"No OCP data found for {accession}.")

    # Update counters
    processed_accessions += 1
    remaining_accessions = total_accessions - processed_accessions

    # Print progress after each accession
    print(f"Progress: {processed_accessions} processed, {remaining_accessions} remaining.")

# Close the connection
conn.close()

# Summary of results
print(f"\nFinished processing {total_accessions} accessions.")
print(f"Successfully retrieved OCP data for {successful_retrievals} accessions.")
print(f"{remaining_accessions} accessions remain to be processed.")
print(f"Results saved in {output_dir}. Errors logged in {error_log} (if any).")
