import ssl
import urllib.request

from bs4 import BeautifulSoup


URL = "https://shidler.hawaii.edu/itm/people"

ssl._create_default_https_context = ssl._create_unverified_context

with urllib.request.urlopen(URL) as response:
    page_html = response.read()

soup = BeautifulSoup(page_html, "html.parser")
print(type(soup))
print("\n".join(soup.prettify().splitlines()[:10]))

people_html = soup.find_all("article", class_="node-faculty")
people = []
for person_html in people_html:
    name = person_html.find("h2")
    if name:
        people.append(name.get_text(" ", strip=True))

print("People:")
for person in people:
    print(person)
print("Number of people found:", len(people))