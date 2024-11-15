import json

# File paths
all2_gas_file = r"C:\Users\samuh\OneDrive\Dokumente\Scotty's Documents\_Programming\vscode_samuel_programming\Finished LDS Talk Archive Website\json\all2_GAs+ap+pr_with_BYU.json"
presidents_file = r"C:\Users\samuh\OneDrive\Dokumente\Scotty's Documents\_Programming\vscode_samuel_programming\Finished LDS Talk Archive Website\json\presidents_w_imgs.json"
output_file = r"C:\Users\samuh\OneDrive\Dokumente\Scotty's Documents\_Programming\vscode_samuel_programming\Finished LDS Talk Archive Website\json\presidents_w_talks.json"

# Load the General Authorities data (all2_GAs+ap+pr_with_BYU.json)
with open(all2_gas_file, 'r') as f:
    all2_gas_data = json.load(f)

# Load the Presidents data (presidents_w_imgs.json)
with open(presidents_file, 'r') as f:
    presidents_data = json.load(f)

# Create a dictionary of the General Authorities by name for easy lookup
ga_dict = {ga['name']: ga for ga in all2_gas_data}

# Prepare the list of presidents with their General Conference and BYU talks
presidents_with_talks = []

# Loop through each president and find if they have corresponding talk data in the General Authorities list
for president in presidents_data:
    president_name = president['name']

    if president_name in ga_dict:
        # Get the corresponding talks from the General Authorities data
        ga_data = ga_dict[president_name]
        presidents_with_talks.append({
            "name": president_name,
            "general_conference_talks": ga_data.get("general_conference_talks", 0),
            "byu_talks": ga_data.get("byu_talks", 0)
        })

# Save the result to a new JSON file
with open(output_file, 'w') as f:
    json.dump(presidents_with_talks, f, indent=4)

print(f"New file 'presidents_w_talks.json' has been created at {output_file}")
