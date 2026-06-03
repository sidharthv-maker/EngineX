import requests
from bs4 import BeautifulSoup
from collections import deque

# Fetch data from WikiPedia!
response = requests.get("https://en.wikipedia.org/wiki/Search_Engine", headers = {"User-Agent": "Mozilla/5.0"})

# Convert the text obtained from the website into a navigate-able tree!
soup = BeautifulSoup(response.text, "html.parser")

# Extract links from the web-page!
links = soup.find_all("a")
print("Link Count:", len(links))

# Print content for 2 page(s)!
articleLinks = deque()
alreadyVisited = set() # Prevent visiting duplicate page(s)!
discovered = set() # Prevent adding duplicate page(s) to queue!
visitedCount = 0
baseLink = "https://en.wikipedia.org"
visitedPages = []

for link in links:
    current = link.get("href")
    if current and current.startswith("/wiki/") and ":" not in current and current not in discovered:
        discovered.add(current)
        articleLinks.append(current)

while visitedCount < 2 and len(articleLinks) != 0:
    current = articleLinks.popleft()
    if current not in alreadyVisited:
        alreadyVisited.add(current)
        fullLink = baseLink + current
        innerResponse = requests.get(fullLink, headers = {"User-Agent": "Mozilla/5.0"})
        innerSoup = BeautifulSoup(innerResponse.text, "html.parser")

        innerParagraphs = innerSoup.find_all("p")
        content = ""
        for passage in innerParagraphs:
            content = content + passage.text + "\n"

        currentPage = {"Title":innerSoup.title.text, "URL":fullLink, "Content":content}
        visitedPages.append(currentPage)

        innerLinks = innerSoup.find_all("a")
        for innerLink in innerLinks:
            innerCurrent = innerLink.get("href")
            if innerCurrent and innerCurrent.startswith("/wiki/") and ":" not in innerCurrent and innerCurrent not in alreadyVisited and innerCurrent not in discovered:
                discovered.add(innerCurrent)
                articleLinks.append(innerCurrent)
        visitedCount = visitedCount + 1

for page in visitedPages:
    print(f"{page['Title']} - {page['URL']}")
    print(page['Content'])