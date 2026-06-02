import requests
from bs4 import BeautifulSoup

# Fetch data from WikiPedia!
response = requests.get("https://en.wikipedia.org/wiki/Search_Engine", headers={"User-Agent": "Mozilla/5.0"})

# Converting the text obtained from the website into a navigate-able tree!
soup = BeautifulSoup(response.text, "html.parser")

# Extracting raw-text, without the HTML tags from the title!
print(soup.title.text)

# Extracting all the paragraph tags!
paragraphs = soup.find_all("p")
print("Paragraph Count:", len(paragraphs))

# Displaying first five paragraphs!
for index in range(min(5, len(paragraphs))):
    text = paragraphs[index].text.strip()
    print("\nParagraph", index + 1)
    print(text)