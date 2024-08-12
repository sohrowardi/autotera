import os
import re

# Define the directory and file paths
html_folder = "html"
output_file = "links.txt"

# Define the list of Terabox domains
terabox_domains = [
    "terabox.com",
    "1024terabox.com",
    "terabox.co",
    "terabox.me",
    "teraboxlink.com"  # Added missing comma
]

# Compile a regex pattern to match only the URLs without trailing HTML tags or extra characters
terabox_pattern = re.compile(
    r'https?://(?:www\.)?(?:' + '|'.join(re.escape(domain) for domain in terabox_domains) + r')[^\s"\']*'
)

# Initialize an empty set to store unique links
terabox_links = set()

# Iterate over all files in the html folder
for filename in os.listdir(html_folder):
    if filename.endswith(".html"):
        file_path = os.path.join(html_folder, filename)
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            # Find all Terabox links in the file content
            links = terabox_pattern.findall(content)
            # Add the found links to the set (to ensure uniqueness)
            terabox_links.update(links)

# Write the collected links to the output file
with open(output_file, "a", encoding="utf-8") as file:
    for link in sorted(terabox_links):
        file.write(link + "\n")

print(f"Collected {len(terabox_links)} unique Terabox links and saved them to {output_file}.")
