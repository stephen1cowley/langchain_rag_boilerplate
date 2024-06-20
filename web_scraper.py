import requests
from bs4 import BeautifulSoup

# The URL of the parent page
url = "https://www.bailii.org/ew/cases/EWHC/Admin/2023/"

# Send a request to fetch the HTML content of the parent page
response = requests.get(url)
html_content = response.content

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Find all <a> tags
a_tags = soup.find_all('a')

# Extract href attributes from the <a> tags
links = [tag.get('href') for tag in a_tags if tag.get('href')]

# Filter the links if needed (e.g., remove links to external sites, duplicates, etc.)
# Here we assume that subpages are relative URLs (not starting with http or https)
subpage_links = [link for link in links if not link.startswith(('http://', 'https://'))]

# Count the number of subpages
num_subpages = len(subpage_links)

print(f"Number of possible HTML subpages: {num_subpages}")

# Optionally, print the list of subpage links
for link in subpage_links:
    print(link)
