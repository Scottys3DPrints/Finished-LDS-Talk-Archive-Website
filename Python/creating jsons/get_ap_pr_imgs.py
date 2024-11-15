import requests
from bs4 import BeautifulSoup
import json

# Define the input JSON file path
input_json_path = r"C:\Users\samuh\OneDrive\Dokumente\Scotty's Documents\_Programming\vscode_samuel_programming\Finished LDS Talk Archive Website\json\ap_pr_w_talks.json"
output_json_path = r"C:\Users\samuh\OneDrive\Dokumente\Scotty's Documents\_Programming\vscode_samuel_programming\Finished LDS Talk Archive Website\json\ap_pr_w_talks_with_images.json"

# Load the JSON file
with open(input_json_path, 'r') as file:
    speakers = json.load(file)

# Base URL of the speakers' list
base_url = "https://speeches.byu.edu/speakers/"

# Function to reformat the name
def reformat_name(name):
    name_parts = name.split(", ")
    return f"{name_parts[1]} {name_parts[0]}" if len(name_parts) == 2 else name

# Function to remove periods from the name for better matching
def clean_name(name):
    return name.replace(".", "").strip()

# Function to search for a speaker and get their image link
def get_image_link(speaker_name):
    # Clean and format the name
    formatted_name = reformat_name(speaker_name)
    cleaned_name = clean_name(formatted_name).lower().replace(' ', '-')
    
    # Search the speakers' page for the cleaned name
    search_url = f"{base_url}{cleaned_name}/"
    print(f"Searching for: {search_url}")
    
    # Send a GET request to the website
    response = requests.get(search_url)
    if response.status_code != 200:
        print(f"Failed to find {speaker_name}")
        return None

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Try to find the image by matching the alt text with the speaker name
    img_tag = soup.find('img', {'alt': lambda x: x and speaker_name.lower() in x.lower()})

    # If image tag is found
    if img_tag:
        img_url = img_tag.get('src')
        return img_url
    else:
        print(f"No image found for {speaker_name}")
        return None

# List to store the updated speaker data
updated_speakers = []

# Iterate through the speakers and get the image link
for speaker in speakers:
    name = speaker['name']
    general_conference_talks = speaker['general_conference_talks']
    byu_talks = speaker['byu_talks']
    
    # Get the image link
    image_link = get_image_link(name)
    
    # Add the speaker's data to the updated list
    updated_speaker = {
        'name': name,
        'general_conference_talks': general_conference_talks,
        'byu_talks': byu_talks,
        'image': image_link if image_link else None  # Set image to None if no image is found
    }
    updated_speakers.append(updated_speaker)

# Save the updated data to a new JSON file
with open(output_json_path, 'w') as output_file:
    json.dump(updated_speakers, output_file, indent=4)

print(f"Image links and talks saved to {output_json_path}")
