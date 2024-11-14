import os
import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Path to the input JSON file
JSON_FILE_PATH = "C:\\Users\\samuh\\OneDrive\\Dokumente\\Scotty's Documents\\_Programming\\vscode_samuel_programming\\Finished LDS Talk Archive Website\\json\\___all2_GAs+ap+pr_with_BYU.json"
# Path to the output JSON file
OUTPUT_FILE_PATH = "BYU_speaker_links.json"

# Function to reformat the speaker's name
def reformat_name(name):
    parts = name.split()
    if len(parts) > 1:
        last_name = parts[-1]
        rest_of_name = " ".join(parts[:-1])
        formatted_name = f"{last_name}, {rest_of_name}"
        print(f"[DEBUG] Reformatted name: {formatted_name}")
        return formatted_name
    return name

# Function to search for the speaker on the BYU website and collect the speaker's URL
def search_and_collect_speaker_url(formatted_name):
    try:
        url = "https://speeches.byu.edu/speakers/"
        print(f"[DEBUG] Fetching {url}")
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            speakers = soup.find_all("a", class_="archive-item__link")

            for speaker in speakers:
                speaker_name = speaker.get_text(strip=True)
                if formatted_name in speaker_name:
                    speaker_url = urljoin(url, speaker['href'])
                    print(f"[INFO] Found speaker: {speaker_name}, URL: {speaker_url}")
                    return speaker_url
    except Exception as e:
        print(f"[ERROR] {e}")
    return None

# Load names from JSON file and create a new JSON file with speaker URLs
def main():
    try:
        with open(JSON_FILE_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)

        speaker_links_data = []

        # Process all names in the list
        for index, entry in enumerate(data):
            name = entry.get("name", "")
            if name:
                print(f"[INFO] Processing speaker {index + 1}: {name}")
                formatted_name = reformat_name(name)
                speaker_url = search_and_collect_speaker_url(formatted_name)
                if speaker_url:  # Only add if the URL is found
                    speaker_links_data.append({
                        "name": name,
                        "speaker_url": speaker_url
                    })

        # Save the collected data to a new JSON file
        with open(OUTPUT_FILE_PATH, "w", encoding="utf-8") as output_file:
            json.dump(speaker_links_data, output_file, indent=4)
        print(f"[INFO] Speaker URLs saved to {OUTPUT_FILE_PATH}")

    except Exception as e:
        print(f"[ERROR] Error reading JSON file: {e}")

if __name__ == "__main__":
    main()
