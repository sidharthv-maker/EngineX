import requests
from bs4 import BeautifulSoup
from collections import deque

# Fetch data from WikiPedia!
response = requests.get("https://en.wikipedia.org/wiki/Search_Engine", headers = {"User-Agent": "Mozilla/5.0"})

# Convert the text obtained from the website into a navigate-able tree!
soup = BeautifulSoup(response.text, "html.parser")

# Extract raw-text, without the HTML tags from the title!
# print(soup.title.text)

# Extract all the paragraph tags!
# paragraphs = soup.find_all("p")
# print("Paragraph Count:", len(paragraphs))

# Displaying first five paragraphs!
# for index in range(min(5, len(paragraphs))):
    # text = paragraphs[index].text.strip()
    # print("\nParagraph", index + 1)
    # print(text)

# Extract links from the web-page!
links = soup.find_all("a")
print("Link Count:", len(links))

# Print link(s) to other articles - first 8 links!
articleLinks = deque()
alreadyVisited = set()
visitedCount = 0
baseLink = "https://en.wikipedia.org"
visitedPages = []

for link in links:
    current = link.get("href")
    if current and current.startswith("/wiki/") and ":" not in current:
        articleLinks.append(current)

while visitedCount < 8 and len(articleLinks) != 0:
    current = articleLinks.popleft()
    if current not in alreadyVisited:
        alreadyVisited.add(current)
        fullLink = baseLink + current
        innerResponse = requests.get(fullLink, headers = {"User-Agent": "Mozilla/5.0"})
        innerSoup = BeautifulSoup(innerResponse.text, "html.parser")

        # print(innerSoup.title.text)
        # print(fullLink)
        currentPage = {"Title":innerSoup.title.text, "URL":fullLink}
        visitedPages.append(currentPage)

        innerLinks = innerSoup.find_all("a")
        for innerLink in innerLinks:
            innerCurrent = innerLink.get("href")
            if innerCurrent and innerCurrent.startswith("/wiki/") and ":" not in innerCurrent and innerCurrent not in alreadyVisited:
                articleLinks.append(innerCurrent)
        visitedCount = visitedCount + 1

for page in visitedPages:
    print(page)