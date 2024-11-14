import os
import time
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

# Constants
BASE_URL = "https://www.churchofjesuschrist.org"
JSON_FILE_PATH = "C:\\Users\\samuh\\OneDrive\\Dokumente\\Scotty's Documents\\_Programming\\vscode_samuel_programming\\Finished LDS Talk Archive Website\\json\\___all2_GAs+ap+pr_with_BYU.json"
OUTPUT_JSON_FILE = "GC_download_links.json"

# Function to extract year and month from the page
def extract_year_and_month(driver):
    try:
        date_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'sc-1r3sor6-0'))
        )
        date_text = date_element.text.strip()
        match = re.search(r'(\w+)\s(\d{4})', date_text)
        if match:
            month = match.group(1)
            year = match.group(2)
            month_numeric = time.strptime(month, '%B').tm_mon
            return year, f"{month_numeric:02d}"
    except Exception as e:
        print(f"[DEBUG] Error extracting year and month: {e}")
    return "Unknown_Year", "Unknown_Month"

# Function to process each talk and collect audio links
def process_talk(driver, talk_url, audio_links):
    try:
        print(f"[DEBUG] Visiting talk URL: {talk_url}")
        driver.get(talk_url)
        time.sleep(1)  # Shorter wait time

        # Close consent banner if present
        try:
            consent_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.ID, 'truste-consent-required'))
            )
            consent_button.click()
            print("[DEBUG] Closed consent banner")
        except:
            print("[DEBUG] No consent banner found")

        # Click the audio button to reveal the link
        audio_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'AudioPlayer__AudioIconButton-sc-2r2ugr-0'))
        )
        audio_button.click()
        print("[DEBUG] Clicked the audio button")

        # Get the audio link
        audio_source = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//source[@type="audio/mpeg"]'))
        )
        audio_url = audio_source.get_attribute('src')
        if audio_url:
            print(f"[INFO] Found audio link: {audio_url}")
            audio_links.append(audio_url)
    except Exception as e:
        print(f"[DEBUG] Error occurred while processing talk: {e}")

# Main function to read JSON, process talks, and save links
def main():
    # Set up Firefox options for headless mode
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    all_audio_links = {}

    try:
        # Load JSON data
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Process all speakers in the JSON data
        for entry in data:
            name = entry['name']
            print(f"[INFO] Processing talks for: {name}")
            audio_links = []

            # Search for the speaker's profile and talks
            search_url = f"{BASE_URL}/study/general-conference/speakers?lang=eng"
            print(f"[DEBUG] Searching for speaker profile at: {search_url}")
            response = requests.get(search_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            speaker_links = soup.find_all('a', href=True, class_=re.compile(r'sc-omeqik-0'))

            normalized_name = ' '.join(name.split()).lower()
            profile_url = None
            for link in speaker_links:
                h4_tag = link.find('h4', class_=re.compile(r'sc-12mz36o-0'))
                if h4_tag and h4_tag.text.strip().lower() == normalized_name:
                    profile_url = urljoin(BASE_URL, link['href'])
                    print(f"[INFO] Found speaker profile URL: {profile_url}")
                    break

            if not profile_url:
                print(f"[DEBUG] Speaker '{name}' not found. Skipping...")
                continue

            # Visit the speaker's profile and process each talk
            response = requests.get(profile_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            talk_links = soup.find_all('a', class_=re.compile(r'sc-omeqik-0'))

            for talk_link in talk_links:
                talk_url = urljoin(BASE_URL, talk_link['href'])
                process_talk(driver, talk_url, audio_links)

            # Save the collected audio links for the speaker
            if audio_links:
                all_audio_links[name] = audio_links

        # Save the collected data to a new JSON file
        with open(OUTPUT_JSON_FILE, 'w', encoding='utf-8') as output_file:
            json.dump(all_audio_links, output_file, indent=4)
        print(f"[INFO] Audio links saved to {OUTPUT_JSON_FILE}")

    except Exception as e:
        print(f"[ERROR] {e}")

    finally:
        driver.quit()

if __name__ == '__main__':
    main()
