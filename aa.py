
# import time
# import logging
# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin, urlparse
# from collections import deque

# # — 설정

# level = 12

# BASE_URL = "https://www.kpedia.jp"
# START_URL = ""

# START_PAGE_INDEX = 1
# LAST_PAGE_INDEX = 1

# if level == 12:  # TOPIC 1,2급
#     START_URL = "https://www.kpedia.jp/p/302-2?nCP=" + str(START_PAGE_INDEX)
#     LAST_PAGE_INDEX = 14
# elif level == 34:# TOPIC 3,4급
#     START_URL = "https://www.kpedia.jp/p/303-2?nCP=" + str(START_PAGE_INDEX)
#     LAST_PAGE_INDEX = 62
    
# else :           # TOPIC 5,6급
#     START_URL = "https://www.kpedia.jp/p/304-2?nCP=" + str(START_PAGE_INDEX)
#     LAST_PAGE_INDEX = 113






# # USER_AGENT = "MyCrawler/1.0 (+https://yourdomain.com)"
# HEADERS = {"User-Agent": ""}
# CRAWL_DELAY = 1.0 # 초 단위
# # #mainContent > table > tbody > tr > td > table:nth-child(9)
# # — 로깅 설정
# logging.basicConfig(
# level=logging.INFO,
# format="%(asctime)s [%(levelname)s] %(message)s",
# datefmt="%Y-%m-%d %H:%M:%S",
# )

# class Crawler:
#     def __init__(self, start_url):
#         self.start_url = start_url
#         self.visited = set()
#         self.queue = deque([start_url])
#         self.domain = urlparse(start_url).netloc

#     def fetch(self, url):
#         """URL의 HTML을 가져와 BeautifulSoup 객체로 반환"""
#         try:
#             response = requests.get(url, headers=HEADERS, timeout=10)
#             response.raise_for_status()
#             logging.info(f"Fetched: {url}")
#             return BeautifulSoup(response.text, "html.parser")
#         except Exception as e:
#             logging.error(f"Failed to fetch {url}: {e}")
#             return None

#     def parse_links(self, soup, base_url):
#         """페이지 내의 모든 내부 링크를 찾아 큐에 추가"""
#         links = []
#         for a in soup.find_all("a", href=True):
#             href = urljoin(base_url, a["href"])
#             parsed = urlparse(href)
#             # 같은 도메인만 크롤
#             if parsed.netloc == self.domain:
#                 clean = parsed.scheme + "://" + parsed.netloc + parsed.path
#                 links.append(clean)
#         return links

#     def process_page(self, soup, url):

#         html_table = soup.select("#mainContent > table.school-course")

#         if (len(html_table) == 0):
#             return
#         html_words = html_table[0].select("tr")

#         for html_word in html_words:
#             html_tds = html_word.select("td")
#             if (len(html_tds) == 0):
#                 continue
#             temp = {}
#             for index in range(3):
#                 html_td = html_tds[index]
#                 td = html_td.text

#                 if (index == 0):
#                     temp["korea"] = td
#                 elif (index == 1):
#                     temp["yomikata"] = td
#                 elif (index == 2):
#                     temp["japan"] = td
#                     html_as = html_td.select("a")

#                     if(len(html_as) != 0):
#                         html_a = html_as[0]
#                         detail_url = BASE_URL + html_a.get("href")
#                         print(detail_url)
#                     else:
#                         print("Error")



#             """페이지 내용에서 원하는 데이터를 추출하거나 저장"""
#             # 예시: 페이지 타이틀 출력
#             title_tag = soup.find("title")
#             title = title_tag.get_text(strip=True) if title_tag else "No Title"
#             logging.info(f"Title @ {url}: {title}")

#             # TODO: 원하는 데이터 파싱 로직을 여기에 추가

#     def run(self, max_pages=100):
#         """최대 max_pages 만큼 페이지를 방문하며 크롤링"""
#         while self.queue and len(self.visited) < max_pages:
#             url = self.queue.popleft()
#             if url in self.visited:
#                 continue

#             self.visited.add(url)
#             soup = self.fetch(url)
#             if soup is None:
#                 continue

# # 데이터 처리
#             self.process_page(soup, url)

# # 링크 수집 및 큐 추가
#             for link in self.parse_links(soup, url):
#                 if link not in self.visited:
#                     self.queue.append(link)

#             time.sleep(CRAWL_DELAY)

# if __name__ == "__main__":
#     crawler = Crawler(START_URL)
#     crawler.run(max_pages=50)




