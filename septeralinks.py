import os
import re
from collections import defaultdict

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the directory and file paths
source_folder = os.path.join(script_dir, "source_folder")  # Ensure the folder name is correct
output_file = os.path.join(script_dir, "links.txt")
archived_file = os.path.join(script_dir, "links_archived.txt")

# Debugging: Print paths to verify correctness
print(f"Script Directory: {script_dir}")
print(f"Source Folder Path: {source_folder}")
print(f"Output File Path: {output_file}")
print(f"Archived File Path: {archived_file}")

# Define the list of Terabox domains
terabox_domains = [
    "terabox.com",
    "1024terabox.com",
    "terabox.co",
    "terabox.me",
    "teraboxlink.com"
]

# Compile a regex pattern to match only the URLs
terabox_pattern = re.compile(
    r'https?://(?:www\.)?(?:' + '|'.join(re.escape(domain) for domain in terabox_domains) + r')[^\s\'"<>]*'
)

# Initialize sets to store links
terabox_links = set()
terabox_links_from_sources = set()
link_occurrences = defaultdict(int)

# Load existing links from the output file into a set
existing_links = set()
if os.path.exists(output_file):
    with open(output_file, "r", encoding="utf-8") as file:
        existing_links.update(file.read().splitlines())

# Load archived links from the archived file into a set
archived_links = set()
if os.path.exists(archived_file):
    with open(archived_file, "r", encoding="utf-8") as file:
        archived_links.update(file.read().splitlines())

# Initialize counters
total_links_found = 0
total_terabox_links = 0
total_duplicates = 0

# Check if source folder exists
if not os.path.isdir(source_folder):
    print(f"Error: The folder '{source_folder}' does not exist.")
    exit()

# Iterate over all files in the source folder
for filename in os.listdir(source_folder):
    if filename.endswith(".html") or filename.endswith(".txt"):
        file_path = os.path.join(source_folder, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            # Find all links in the file content
            links = re.findall(r'https?://[^\s\'"<>]+', content)
            total_links_found += len(links)
            
            # Filter Terabox links
            terabox_links_in_file = set(terabox_pattern.findall(content))
            total_terabox_links += len(terabox_links_in_file)
            
            # Count occurrences and duplicates
            for link in terabox_links_in_file:
                link_occurrences[link] += 1
            
            # Update the set of Terabox links found in sources
            terabox_links_from_sources.update(terabox_links_in_file)
            
            # Add unique Terabox links to the set
            terabox_links.update(terabox_links_in_file)

# Calculate total duplicates
total_duplicates = sum(1 for count in link_occurrences.values() if count > 1)

# Check for existing links
existing_in_output = len(terabox_links & existing_links)
existing_in_archived = len(terabox_links & archived_links)

# Remove Terabox links that are already in the archived file or output file
terabox_links.difference_update(archived_links)
terabox_links.difference_update(existing_links)

# Write the collected Terabox links to the output file, ensuring no duplicates
with open(output_file, "a", encoding="utf-8") as file:
    for link in sorted(terabox_links):
        file.write(link + "\n")

# Calculate the number of new links added
new_links_count = len(terabox_links)

# Print the statistics
print(f"Total links found in source files: {total_links_found}")
print(f"Total Terabox links found: {total_terabox_links}")
print()
print(f"Total duplicated links within source files: {total_duplicates}")
print(f"Existing Terabox links in links.txt: {existing_in_output}")
print(f"Existing Terabox links in links_archived.txt: {existing_in_archived}")
print()
print(f"New links added to links.txt: {new_links_count}")

# Keep the terminal open until the user presses Enter
input("Press Enter to exit...")
