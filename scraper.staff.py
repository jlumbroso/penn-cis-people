import json
import re

import bs4
import requests

URL = "https://www.cis.upenn.edu/staff/"

response = requests.get(URL)
soup = bs4.BeautifulSoup(response.content, "html.parser")

# Find all staff members
staff_members = soup.select(".tmm_member")

staff_list = []

for member in staff_members:
    name = member.select_one(".tmm_names").get_text(strip=False)
    job_title = member.select_one(".tmm_job").get_text(strip=True)
    description = member.select_one(".tmm_desc").get_text(strip=False)

    # Attempt to extract image URL
    photo_div = member.find("div", class_="tmm_photo")
    photo_url = None
    if photo_div:
        style_content = photo_div.get("style", "")
        match = re.search(r"background: url\((.*?)\);", style_content)
        if match:
            photo_url = match.group(1)

    # Extracting contact details
    contact_details = {}

    for line in description.split("\n"):
        if "Office" in line:
            contact_details["Office"] = line.split(":")[1].strip()
        elif "Phone" in line:
            contact_details["Phone"] = line.split(":")[1].strip()
        elif "Fax" in line:
            contact_details["Fax"] = line.split(":")[1].strip()
        elif "Email" in line:
            contact_details["Email"] = line.split(":")[1].strip()

    staff_list.append(
        {
            "name": name,
            "title": job_title,
            "image_url": photo_url,
            "contact": contact_details,
        }
    )

# Convert the list to JSON
staff_json = json.dumps(staff_list, indent=4)

print(staff_json)
