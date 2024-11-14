import json

# Path to your JSON file
file_path = r"C:\Users\samuh\OneDrive\Dokumente\Scotty's Documents\_Programming\vscode_samuel_programming\Finished LDS Talk Archive Website\GC_download_links.json"

# Function to add "?download=true" to each link
def add_download_param_to_links(file_path):
    try:
        # Open the file and load the data
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Iterate over each speaker and their corresponding links
        for speaker, links in data.items():
            # Modify each link in the list of links
            for i in range(len(links)):
                links[i] = links[i] + "?download=true"
        
        # Write the updated data back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

        print("Links updated successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function
add_download_param_to_links(file_path)
