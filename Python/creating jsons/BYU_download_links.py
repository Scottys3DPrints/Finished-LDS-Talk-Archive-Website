import os
import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Path to the input JSON file
JSON_FILE_PATH = "C:\\Users\\samuh\\OneDrive\\Dokumente\\Scotty's Documents\\_Programming\\vscode_samuel_programming\\Finished LDS Talk Archive Website\\json\\___all2_GAs+ap+pr_with_BYU.json"
# Path to the output JSON file
OUTPUT_FILE_PATH = "BYU_download_links.json"

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

# Function to search for the speaker on the BYU website and collect MP3 download links
def search_and_collect_mp3_links(formatted_name):
    links = []
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
                    print(f"[DEBUG] Found speaker: {speaker_name}, visiting {speaker_url}")

                    # Visit the speaker's page to get MP3 download links
                    speaker_response = requests.get(speaker_url)
                    if speaker_response.status_code == 200:
                        speaker_soup = BeautifulSoup(speaker_response.content, "html.parser")
                        talks = speaker_soup.find_all('article', class_="card card--reduced")

                        for talk in talks:
                            # Extract the MP3 download link
                            mp3_link_tag = talk.find('a', class_="download-links__option--available", string=lambda text: "MP3" in text)
                            if mp3_link_tag:
                                mp3_link = urljoin(speaker_url, mp3_link_tag['href'])
                                print(f"[INFO] MP3 link found: {mp3_link}")
                                links.append(mp3_link)
                        return links
    except Exception as e:
        print(f"[ERROR] {e}")
    return links

# Load names from JSON file and create a new JSON file with download links
def main():
    try:
        with open(JSON_FILE_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)

        download_links_data = []

        # Process all names in the list
        for index, entry in enumerate(data):
            name = entry.get("name", "")
            if name:
                print(f"[INFO] Processing speaker {index + 1}: {name}")
                formatted_name = reformat_name(name)
                links = search_and_collect_mp3_links(formatted_name)
                if links:  # Only add if there are download links
                    download_links_data.append({
                        "name": name,
                        "links": links
                    })

        # Save the collected data to a new JSON file
        with open(OUTPUT_FILE_PATH, "w", encoding="utf-8") as output_file:
            json.dump(download_links_data, output_file, indent=4)
        print(f"[INFO] Download links saved to {OUTPUT_FILE_PATH}")

    except Exception as e:
        print(f"[ERROR] Error reading JSON file: {e}")

if __name__ == "__main__":
    main()
