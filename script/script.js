// Variables for pagination
let currentPage = 1;
const itemsPerPage = 15;
let membersData = []; // Stores all members data for searching and pagination
let isAlphabeticalPage = false; // Flag to check if the alphabetical page is active

// Function to handle download when the button is clicked
function handleDownloadClick(event) {
    const talkCard = event.target.closest('.talk-card');
    if (!talkCard) {
        console.error("Talk card not found.");
        return;
    }

    const nameElement = talkCard.querySelector('h3');
    if (!nameElement) {
        console.error("Name element not found in talk-card.");
        return;
    }

    const name = nameElement.textContent.trim(); // Speaker name

    // Checkboxes for GC and BYU
    const gcDownloadCheckbox = talkCard.querySelector("#gc_download");
    const byuDownloadCheckbox = talkCard.querySelector("#byu_download");

    const gcDownload = gcDownloadCheckbox.checked;
    const byuDownload = byuDownloadCheckbox.checked;

    // URLs arrays to hold download links
    let downloadLinks = [];

    // Fetch GC download links if the checkbox is checked
    if (gcDownload) {
        fetch('GC_download_links.json')
            .then(response => response.json())
            .then(data => {
                if (data[name]) {
                    downloadLinks = downloadLinks.concat(data[name]);
                } else {
                    console.log(`No GC links found for ${name}`);
                }

                // If BYU download is also checked, fetch and open the speaker's URL
                if (byuDownload) {
                    fetchAndOpenBYUSpeakerUrl(name, downloadLinks);
                } else {
                    // Trigger download for GC links
                    triggerDownload(downloadLinks);
                }
            })
            .catch(error => console.error('Error fetching GC links:', error));
    }
    // If BYU download is checked but GC isn't, fetch and open the speaker's URL
    else if (byuDownload) {
        fetchAndOpenBYUSpeakerUrl(name);
    } else {
        console.log("No download option selected.");
    }

    // Uncheck the checkboxes
    gcDownloadCheckbox.checked = false;
    byuDownloadCheckbox.checked = false;
}

// Function to fetch and open the BYU speaker URL
function fetchAndOpenBYUSpeakerUrl(name, gcLinks = []) {
    fetch('json/BYU_speaker_links.json')
        .then(response => response.json())
        .then(data => {
            const speakerData = data.find(entry => entry.name === name);
            if (speakerData && speakerData.speaker_url) {
                // Open the speaker URL in a new tab
                window.open(speakerData.speaker_url, '_blank');
            } else {
                console.log(`No BYU speaker URL found for ${name}`);
            }

            // If there are GC links, trigger their download
            if (gcLinks.length > 0) {
                triggerDownload(gcLinks);
            }
        })
        .catch(error => console.error('Error fetching BYU speaker links:', error));
}

// Function to trigger the download action for the collected GC links
function triggerDownload(links) {
    if (links.length === 0) {
        console.error("No links available for download.");
        return;
    }

    // Open each URL in a new tab
    links.forEach(link => {
        window.open(link, '_blank');
    });
}

// Function to load "Current" members from the JSON file
function loadCurrentMembers() {
    isAlphabeticalPage = false; // Set the flag to false
    fetch('json/current_with_byu.json')
        .then(response => response.json())
        .then(data => {
            membersData = data; // Store all members data for searching
            displayMembers(data, true);
            removePagination();
        })
        .catch(error => console.error('Error loading current members:', error));
}

// Function to load and sort all General Authorities alphabetically by last name, with pagination
function loadAlphabeticalMembers() {
    isAlphabeticalPage = true; // Set the flag to true
    fetch('json/all2_GAs+ap+pr_with_BYU.json')
        .then(response => response.json())
        .then(data => {
            membersData = data.sort((a, b) => {
                const lastNameA = a.name.split(" ").pop().toLowerCase();
                const lastNameB = b.name.split(" ").pop().toLowerCase();
                return lastNameA.localeCompare(lastNameB);
            });

            displayPaginatedMembers();
        })
        .catch(error => console.error('Error loading all General Authorities:', error));
}

// Function to load and display prophets from the JSON file
function loadProphets() {
    isAlphabeticalPage = false; // Set the flag to false
    fetch('json/ap_pr_w_talks_with_images.json') // This loads the prophets and apostles data
        .then(response => response.json())
        .then(data => {
            membersData = data.sort((a, b) => {
                return a.name.toLowerCase().localeCompare(b.name.toLowerCase()); // Sort alphabetically by name
            }); // Sorting the data alphabetically by name
            displayMembers(data, true); // Display the members in the talks container
            removePagination(); // Remove pagination if it's not needed
        })
        .catch(error => console.error('Error loading prophets:', error));
}

// Function to display members with pagination for the "Alphabetical" button only
function displayPaginatedMembers() {
    const totalPages = Math.ceil(membersData.length / itemsPerPage);

    // Get the current page's members
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const currentMembers = membersData.slice(startIndex, endIndex);

    displayMembers(currentMembers, false);
    createPaginationControls(totalPages);
}

// Function to create pagination controls
function createPaginationControls(totalPages) {
    const paginationContainer = document.getElementById('pagination-container') || document.createElement('div');
    paginationContainer.id = 'pagination-container';
    paginationContainer.innerHTML = '';

    if (currentPage > 1) {
        const prevButton = document.createElement('button');
        prevButton.textContent = 'Previous';
        prevButton.classList.add('pagination-button'); // Add class

        prevButton.addEventListener('click', () => {
            currentPage--;
            displayPaginatedMembers();
        });
        paginationContainer.appendChild(prevButton);
    }

    if (currentPage < totalPages) {
        const nextButton = document.createElement('button');
        nextButton.textContent = 'Next';
        nextButton.classList.add('pagination-button'); // Add class

        nextButton.addEventListener('click', () => {
            currentPage++;
            displayPaginatedMembers();
        });
        paginationContainer.appendChild(nextButton);
    }

    document.querySelector('.main_container').appendChild(paginationContainer);
}

// Function to remove pagination controls
function removePagination() {
    const paginationContainer = document.getElementById('pagination-container');
    if (paginationContainer) {
        paginationContainer.remove();
    }
}

// Function to display members on the page
function displayMembers(members, showImages) {
    const talksContainer = document.getElementById('talks-container');
    talksContainer.innerHTML = ''; // Clear the container

    members.forEach(member => {
        const talkCard = document.createElement('div');
        talkCard.className = 'talk-card grid_talk_card';

        if (showImages && !isAlphabeticalPage) { // Ensure images are never shown on the alphabetical page
            const img = document.createElement('img');
            img.src = member.image || '';
            img.alt = member.name;
            img.className = 'ga_img';
            talkCard.appendChild(img);
        }

        const speakerInfo = document.createElement('div');
        speakerInfo.className = 'flex_column flex_speaker grid_talk_a1';
        speakerInfo.innerHTML = `
            <h3>${member.name}</h3>
        `;

        talkCard.appendChild(speakerInfo);

        const gcInfo = document.createElement('div');
        gcInfo.className = 'flex_column grid_talk_a2';
        gcInfo.innerHTML = `
            <h4>General Conference</h4>
            <p>${member.general_conference_talks || 'Amount'}</p>
        `;

        const byuInfo = document.createElement('div');
        byuInfo.className = 'flex_column grid_talk_a3';
        byuInfo.innerHTML = `
            <h4>BYU</h4>
            <p>${member.byu_talks || 'Amount'}</p>
        `;

        const downloadContainer = document.createElement('div');
        downloadContainer.className = 'flex_column flex_download grid_talk_a4';
        downloadContainer.innerHTML = `
            <div class="checkbox-container">
                <input type="checkbox" id="gc_download">
                <label for="gc_download">Download General Conference</label>
            </div>
            <div class="checkbox-container">
                <input type="checkbox" id="byu_download">
                <label for="byu_download">Download BYU</label>
            </div>
            <button class="download-button">Download</button>
        `;

        talkCard.appendChild(gcInfo);
        talkCard.appendChild(byuInfo);
        talkCard.appendChild(downloadContainer);
        talksContainer.appendChild(talkCard);
    });

    // Reattach event listeners to the new download buttons
    document.querySelectorAll('.download-button').forEach(button => {
        button.addEventListener('click', handleDownloadClick);
    });
}

// Search function to filter members based on the input text
function searchTalks() {
    const searchInput = document.getElementById('search-input').value.toLowerCase();
    const filteredMembers = membersData.filter(member =>
        member.name.toLowerCase().includes(searchInput)
    );

    // Never show images on the alphabetical page, even during a search
    displayMembers(filteredMembers, !isAlphabeticalPage);
}

// Event listeners for buttons
document.getElementById('current-button').addEventListener('click', loadCurrentMembers);
document.getElementById('alphabetical-button').addEventListener('click', loadAlphabeticalMembers);
document.getElementById('popular-button').addEventListener('click', loadProphets);
document.getElementById('search-input').addEventListener('input', searchTalks);

// Load "Current" members by default when the page is loaded
document.addEventListener('DOMContentLoaded', () => {
    loadCurrentMembers(); // Ensure "Current" members are loaded when the page loads
});
