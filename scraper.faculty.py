import json

import bs4
import orjson
import requests

URL = "https://directory.seas.upenn.edu/computer-and-information-science/#new_tab"

response = requests.get(URL)
soup = bs4.BeautifulSoup(response.content, "html.parser")

# Find all faculty entries
faculty_entries = soup.find_all(class_="SingleStaffList")

faculty_list = []

for entry in faculty_entries:
    faculty = {}

    # Extract name
    name = entry.find(class_="StaffListName").a.text.strip()
    faculty["name"] = name

    # Extract image URL
    image_url = entry.find(class_="StaffListPhoto").a.img["src"]
    faculty["image_url"] = image_url

    # Extract and clean titles
    raw_titles = entry.find(class_="StaffListTitles").text.split("\n")
    titles = [title.strip() for title in raw_titles if title.strip()]
    faculty["titles"] = titles

    # Extract email (if available)
    email_icon = entry.find("i", class_="sls-icon email")
    if email_icon:
        email = email_icon.find_parent("a")["href"].replace("mailto:", "").strip()
        faculty["email"] = email

    faculty_list.append(faculty)

# Convert the list to JSON format
faculty_json = json.dumps(faculty_list, indent=4)

print(faculty_json)
