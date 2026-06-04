import requests
from bs4 import BeautifulSoup
from collections import deque
from db import connect, init_db

# Initiate the data-base!
init_db()
connection = connect()

articleLinks = deque() # Process link(s) in breadth-first manner!
alreadyVisited = set() # Prevent visiting duplicate page(s)!
discovered = set() # Prevent adding duplicate page(s) to queue!
visitedCount = 0 # Limit number of pages visited!
baseLink = "https://en.wikipedia.org"

# Fetch data from WikiPedia!
seed = ["https://en.wikipedia.org/wiki/Search_engine", "https://en.wikipedia.org/wiki/Web_crawler", "https://en.wikipedia.org/wiki/PageRank", "https://en.wikipedia.org/wiki/Information_retrieval"]
for current in seed:
    articleLinks.append(current.replace(baseLink, ""))
    discovered.add(current.replace(baseLink, ""))

while visitedCount < 10 and len(articleLinks) != 0:
    current = articleLinks.popleft()
    if current not in alreadyVisited:
        alreadyVisited.add(current)
        fullLink = baseLink + current
        print(f"Crawling: {fullLink}")
        response = requests.get(fullLink, headers = {"User-Agent": "Mozilla/5.0"})

        # Only visit page if status code is 200, else don't!
        if response.status_code != 200:
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = soup.find_all("p")
        content = ""
        for passage in paragraphs:
            content = content + passage.text + "\n"

        connection.execute("""INSERT OR IGNORE INTO pages(url, title, content) VALUES(?, ?, ?)""", (fullLink, soup.title.text, content))

        links = soup.find_all("a")
        for link in links:
            current = link.get("href")
            if current and current.startswith("/wiki/") and ":" not in current and current not in alreadyVisited and current not in discovered:
                discovered.add(current)
                articleLinks.append(current)
        visitedCount = visitedCount + 1

connection.commit()
connection.close()