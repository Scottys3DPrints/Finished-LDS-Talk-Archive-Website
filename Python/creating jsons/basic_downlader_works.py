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
DOWNLOAD_DIR = "C:\\_Download Talk Test Folder"
JSON_FILE_PATH = "C:\\Users\\samuh\\OneDrive\\Dokumente\\Scotty's Documents\\_Programming\\vscode_samuel_programming\\Finished LDS Talk Archive Website\\json\\___all2_GAs+ap+pr_with_BYU.json"

# Function to download and save audio
def download_audio(audio_url, filename):
    try:
        response = requests.get(audio_url)
        response.raise_for_status()
        file_path = os.path.join(DOWNLOAD_DIR, filename)
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"Downloaded and saved: {file_path}")
    except Exception as e:
        print(f"Error downloading audio: {e}")

# Function to extract year and month from the page
def extract_year_and_month(driver):
    try:
        date_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'sc-1r3sor6-0'))
        )
        date_text = date_element.text.strip()
        match = re.search(r'(\w+)\s(\d{4})', date_text)
        if match:
            month = match.group(1)
            year = match.group(2)
            month_numeric = time.strptime(month, '%B').tm_mon
            month_str = f"{month_numeric:02d}"
            return year, month_str
        else:
            return "Unknown_Year", "Unknown_Month"
    except Exception as e:
        print(f"Error extracting year and month: {e}")
        return "Unknown_Year", "Unknown_Month"

# Function to process each talk
def process_talk(driver, talk_url, speaker):
    try:
        driver.get(talk_url)
        time.sleep(2)
        try:
            consent_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, 'truste-consent-required'))
            )
            time.sleep(1)
            consent_button.click()
            print("Consent banner closed")
        except:
            print("No consent banner found")

        audio_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'AudioPlayer__AudioIconButton-sc-2r2ugr-0'))
        )
        time.sleep(1)
        audio_button.click()
        print("Audio button clicked successfully!")

        audio_source = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//source[@type="audio/mpeg"]'))
        )
        audio_url = audio_source.get_attribute('src')

        talk_title_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h1'))
        )
        talk_title = talk_title_element.text.strip()
        print(f"Talk title: {talk_title}")

        if audio_url:
            print(f"Found audio link: {audio_url}")
            year, month = extract_year_and_month(driver)
            sanitized_talk_title = re.sub(r'[\\/*?:"<>|]', "", talk_title.replace(" ", "_"))
            filename = f"{year}_{month}_{sanitized_talk_title}_{speaker}.mp3"
            download_audio(audio_url, filename)
        else:
            print("Audio link not found.")
    except Exception as e:
        print(f"Error occurred while processing talk: {e}")

# Main function to read JSON and process talks
def main():
    # Set up Firefox options for headless mode
    options = Options()
    options.add_argument("--headless")  # Run Firefox in headless mode
    options.add_argument("--no-sandbox")  # Ensure it runs smoothly in some environments
    options.add_argument("--disable-gpu")  # Disable GPU rendering if necessary
    options.add_argument("--window-size=1920x1080")  # Set a default window size

    # Initialize Firefox WebDriver with headless options
    driver = webdriver.Firefox(options=options)  # Ensure geckodriver is installed and in your PATH

    try:
        # Load JSON data
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Process the first 10 speakers
        for entry in data[:10]:
            name = entry['name']
            print(f"Processing talks for: {name}")

            # Search for the speaker's profile and talks
            search_url = f"{BASE_URL}/study/general-conference/speakers?lang=eng"
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
                    print(f"Speaker profile URL found: {profile_url}")
                    break

            if not profile_url:
                print(f"Speaker '{name}' not found.")
                continue

            # Visit the speaker's profile and process each talk
            response = requests.get(profile_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            talk_links = soup.find_all('a', class_=re.compile(r'sc-omeqik-0'))

            for talk_link in talk_links:
                talk_url = urljoin(BASE_URL, talk_link['href'])
                process_talk(driver, talk_url, name)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        driver.quit()

if __name__ == '__main__':
    main()
