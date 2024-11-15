import json

# File paths
all2_gas_file = r"C:\Users\samuh\OneDrive\Dokumente\Scotty's Documents\_Programming\vscode_samuel_programming\Finished LDS Talk Archive Website\json\all2_GAs+ap+pr_with_BYU.json"
apostles_file = r"C:\Users\samuh\OneDrive\Dokumente\Scotty's Documents\_Programming\vscode_samuel_programming\Finished LDS Talk Archive Website\json\apostles.json"
output_file = r"C:\Users\samuh\OneDrive\Dokumente\Scotty's Documents\_Programming\vscode_samuel_programming\Finished LDS Talk Archive Website\json\apostles_w_talks.json"

# Load the General Authorities data (all2_GAs+ap+pr_with_BYU.json)
with open(all2_gas_file, 'r') as f:
    all2_gas_data = json.load(f)

# Load the Apostles data (apostles.json)
with open(apostles_file, 'r') as f:
    apostles_data = json.load(f)

# Create a dictionary of the General Authorities by name for easy lookup
ga_dict = {ga['name']: ga for ga in all2_gas_data}

# Prepare the list of apostles with their General Conference and BYU talks
apostles_with_talks = []

# Loop through each apostle and find if they have corresponding talk data in the General Authorities list
for apostle in apostles_data:
    apostle_name = apostle['name']

    if apostle_name in ga_dict:
        # Get the corresponding talks from the General Authorities data
        ga_data = ga_dict[apostle_name]
        apostles_with_talks.append({
            "name": apostle_name,
            "general_conference_talks": ga_data.get("general_conference_talks", 0),
            "byu_talks": ga_data.get("byu_talks", 0)
        })

# Save the result to a new JSON file
with open(output_file, 'w') as f:
    json.dump(apostles_with_talks, f, indent=4)

print(f"New file 'apostles_w_talks.json' has been created at {output_file}")
