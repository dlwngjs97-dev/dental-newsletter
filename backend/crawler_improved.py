import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re
from database import Database

class DentalNewsCrawler:
    def __init__(self):
        self.db = Database()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def crawl_all(self):
        """모든 언론사 크롤링"""
        print("=== 치과 뉴스레터 크롤링 시작 ===")
        print(f"시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        sources = [
            ('치의신보', self.crawl_generic, 'https://www.dailydental.co.kr', '/news/articleList.html?sc_section_code=S1N1'),
            ('치과신문', self.crawl_generic, 'https://www.dentalnews.or.kr', '/news/articleList.html?sc_section_code=S1N1'),
            ('덴탈아리랑', self.crawl_generic, 'https://www.dentalarirang.com', '/news/articleList.html?sc_section_code=S1N1')
        ]

        total_new = 0
        for source_name, crawl_func, base_url, path in sources:
            print(f"[{source_name}] 크롤링 중...")
            try:
                new_count = crawl_func(source_name, base_url, path)
                total_new += new_count
                print(f"[{source_name}] {new_count}개 신규 기사 수집\n")
            except Exception as e:
                print(f"[{source_name}] 오류 발생: {str(e)}\n")

            time.sleep(2)

        print(f"=== 크롤링 완료: 총 {total_new}개 신규 기사 ===")

        exported = self.db.export_to_json()
        print(f"JSON 파일 업데이트: {exported}개 기사")

        return total_new

    def crawl_generic(self, source_name, base_url, path):
        """범용 크롤링 함수"""
        url = base_url + path
        new_articles = 0

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')

            # 여러 셀렉터 패턴 시도
            selectors = [
                'ul.section-list li',
                '.article-list li',
                '.news-list li',
                'ul li.article',
                'div.list-content ul li',
                '.section-content ul li',
            ]

            articles = []
            for selector in selectors:
                articles = soup.select(selector)
                if len(articles) > 5:  # 최소 5개 이상 발견
                    print(f"   ✅ 패턴 발견: {selector} ({len(articles)}개)")
                    break

            if not articles:
                print(f"   ⚠️ 기사 목록을 찾을 수 없습니다")
                return 0

            for article in articles[:20]:  # 최신 20개만
                try:
                    # 제목과 링크 찾기 (여러 패턴 시도)
                    title_elem = None
                    link = None

                    title_selectors = [
                        'a.list-titles',
                        '.titles a',
                        'a[href*="article"]',
                        'h2 a',
                        'h3 a',
                        '.title a',
                        'a',
                    ]

                    for ts in title_selectors:
                        title_elem = article.select_one(ts)
                        if title_elem and title_elem.get_text(strip=True):
                            break

                    if not title_elem:
                        continue

                    title = title_elem.get_text(strip=True)
                    link_href = title_elem.get('href', '')

                    if not link_href or 'article' not in link_href.lower():
                        continue

                    article_url = base_url + link_href if link_href.startswith('/') else link_href

                    # 썸네일 찾기
                    thumbnail = ''
                    img_selectors = [
                        'img.list-img',
                        '.thumb img',
                        '.thumbnail img',
                        'img',
                    ]

                    for img_sel in img_selectors:
                        img_tag = article.select_one(img_sel)
                        if img_tag and img_tag.get('src'):
                            src = img_tag['src']
                            if src.startswith('/'):
                                thumbnail = base_url + src
                            elif src.startswith('http'):
                                thumbnail = src
                            break

                    # 날짜 찾기
                    published_date = ''
                    date_selectors = [
                        '.list-dated',
                        '.date',
                        '.byline em',
                        'time',
                        'span.date',
                    ]

                    for date_sel in date_selectors:
                        date_tag = article.select_one(date_sel)
                        if date_tag:
                            published_date = date_tag.get_text(strip=True)
                            break

                    if not published_date:
                        published_date = datetime.now().strftime('%Y-%m-%d')

                    # 기사 상세 페이지에서 본문 가져오기
                    content = self._fetch_article_content(article_url)

                    article_data = {
                        'source': source_name,
                        'title': title,
                        'url': article_url,
                        'thumbnail': thumbnail,
                        'content': content,
                        'published_date': published_date,
                        'category': '치과'
                    }

                    if self.db.insert_article(article_data):
                        new_articles += 1
                        print(f"   📰 수집: {title[:40]}...")

                    time.sleep(0.5)

                except Exception as e:
                    print(f"   ⚠️ 기사 처리 오류: {str(e)}")
                    continue

        except Exception as e:
            print(f"   ❌ 크롤링 오류: {str(e)}")

        return new_articles

    def _fetch_article_content(self, url):
        """기사 본문 가져오기"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')

            # 본문 셀렉터 (여러 패턴 시도)
            content_selectors = [
                'article .article-view-content-div',
                '.article-content',
                '.news-content',
                '#article-view-content-div',
                '.view-content',
            ]

            for selector in content_selectors:
                content_tag = soup.select_one(selector)
                if content_tag:
                    # 불필요한 태그 제거
                    for tag in content_tag.select('script, style, .ad, .related, .share'):
                        tag.decompose()

                    text = content_tag.get_text(strip=True)
                    if len(text) > 100:  # 최소 100자 이상
                        return text[:2000]  # 2000자까지만

        except:
            pass

        return ''


if __name__ == '__main__':
    crawler = DentalNewsCrawler()
    crawler.crawl_all()
