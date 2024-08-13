import os
import re

# Define the directory and file paths
html_folder = "html"
output_file = "links.txt"
archived_file = "links_archived.txt"

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

# Iterate over all files in the html folder
total_links_found = 0
for filename in os.listdir(html_folder):
    if filename.endswith(".html"):
        file_path = os.path.join(html_folder, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            # Find all Terabox links in the file content
            links = terabox_pattern.findall(content)
            total_links_found += len(links)
            
            # Update the set of Terabox links
            terabox_links.update(links)

# Calculate how many of the total links are Terabox links
total_terabox_links = len(terabox_links)

# Load existing links from the output file into the set
existing_links = set()
if os.path.exists(output_file):
    with open(output_file, "r", encoding="utf-8") as file:
        existing_links.update(file.read().splitlines())

# Load archived links from the archived file into a set
archived_links = set()
if os.path.exists(archived_file):
    with open(archived_file, "r", encoding="utf-8") as file:
        archived_links.update(file.read().splitlines())

# Determine the new unique Terabox links that need to be added
already_existing_links = terabox_links.intersection(existing_links).union(terabox_links.intersection(archived_links))
already_existing_links_count = len(already_existing_links)

new_links = terabox_links.difference(existing_links).difference(archived_links)
new_links_count = len(new_links)

# Write the collected Terabox links to the output file, ensuring no duplicates
with open(output_file, "a", encoding="utf-8") as file:
    for link in sorted(new_links):
        file.write(link + "\n")

# Print the statistics
print(f"Total links found in HTML files: {total_links_found}")
print(f"Total unique Terabox links found: {total_terabox_links}")
print(f"Already exist links.txt and links_archived.txt: {already_existing_links_count}")
print(f"New links added to links.txt: {new_links_count}")
