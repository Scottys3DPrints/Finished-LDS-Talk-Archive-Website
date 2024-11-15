import json

# File paths
presidents_file = r"C:\Users\samuh\OneDrive\Dokumente\Scotty's Documents\_Programming\vscode_samuel_programming\Finished LDS Talk Archive Website\json\presidents_w_talks.json"
apostles_file = r"C:\Users\samuh\OneDrive\Dokumente\Scotty's Documents\_Programming\vscode_samuel_programming\Finished LDS Talk Archive Website\json\apostles_w_talks.json"
output_file = r"C:\Users\samuh\OneDrive\Dokumente\Scotty's Documents\_Programming\vscode_samuel_programming\Finished LDS Talk Archive Website\json\ap_pr_w_talks.json"  # Updated output file name

# Load the Presidents with talks data (presidents_w_talks.json)
with open(presidents_file, 'r') as f:
    presidents_data = json.load(f)

# Load the Apostles with talks data (apostles_w_talks.json)
with open(apostles_file, 'r') as f:
    apostles_data = json.load(f)

# Combine the two datasets (presidents and apostles)
combined_data = presidents_data + apostles_data

# Save the combined data to the new JSON file (ap_pr_w_talks.json)
with open(output_file, 'w') as f:
    json.dump(combined_data, f, indent=4)

print(f"New file 'ap_pr_w_talks.json' has been created at {output_file}")
