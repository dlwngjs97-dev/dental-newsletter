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
            ('치의신보', self.crawl_dailydental),
            ('치과신문', self.crawl_dentalnews),
            ('덴탈아리랑', self.crawl_dentalarirang)
        ]

        total_new = 0
        for source_name, crawl_func in sources:
            print(f"[{source_name}] 크롤링 중...")
            try:
                new_count = crawl_func()
                total_new += new_count
                print(f"[{source_name}] {new_count}개 신규 기사 수집\n")
            except Exception as e:
                print(f"[{source_name}] 오류 발생: {str(e)}\n")

            time.sleep(2)

        print(f"=== 크롤링 완료: 총 {total_new}개 신규 기사 ===")

        exported = self.db.export_to_json()
        print(f"JSON 파일 업데이트: {exported}개 기사")

        return total_new

    def crawl_dailydental(self):
        """치의신보 - 메인 페이지에서 최신 기사"""
        base_url = 'https://www.dailydental.co.kr'
        main_url = base_url

        new_articles = 0

        try:
            response = requests.get(main_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')

            # 모든 기사 링크 찾기 (article.html 패턴)
            all_links = soup.find_all('a', href=re.compile(r'/news/article\.html\?no=\d+'))

            # 중복 제거
            seen_urls = set()
            unique_articles = []

            for link in all_links:
                href = link.get('href')
                full_url = base_url + href if href.startswith('/') else href

                if full_url not in seen_urls:
                    title = link.get_text(strip=True)
                    if len(title) > 10:  # 제목이 충분히 긴 경우만
                        seen_urls.add(full_url)
                        unique_articles.append({
                            'url': full_url,
                            'title': title,
                            'link_elem': link
                        })

            print(f"   발견: {len(unique_articles)}개 기사")

            for article_info in unique_articles[:15]:  # 최신 15개
                try:
                    # 썸네일 찾기 (링크 근처)
                    thumbnail = ''
                    parent = article_info['link_elem'].parent
                    if parent:
                        img = parent.find('img')
                        if not img and parent.parent:
                            img = parent.parent.find('img')

                        if img and img.get('src'):
                            src = img['src']
                            if src.startswith('/'):
                                thumbnail = base_url + src
                            elif src.startswith('http'):
                                thumbnail = src

                    # 기사 상세 페이지에서 내용 가져오기
                    content = self._fetch_content(article_info['url'])

                    article_data = {
                        'source': '치의신보',
                        'title': article_info['title'],
                        'url': article_info['url'],
                        'thumbnail': thumbnail,
                        'content': content,
                        'published_date': datetime.now().strftime('%Y-%m-%d'),
                        'category': '치과'
                    }

                    if self.db.insert_article(article_data):
                        new_articles += 1
                        print(f"   ✅ {article_info['title'][:40]}")

                    time.sleep(0.5)

                except Exception as e:
                    print(f"   ⚠️ 기사 처리 오류: {str(e)}")
                    continue

        except Exception as e:
            print(f"   ❌ 크롤링 오류: {str(e)}")

        return new_articles

    def crawl_dentalnews(self):
        """치과신문 - 메인 페이지에서 최신 기사"""
        base_url = 'https://www.dentalnews.or.kr'
        main_url = base_url

        new_articles = 0

        try:
            response = requests.get(main_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')

            # 모든 기사 링크 찾기
            all_links = soup.find_all('a', href=re.compile(r'/news/article\.html\?no=\d+'))

            seen_urls = set()
            unique_articles = []

            for link in all_links:
                href = link.get('href')
                full_url = base_url + href if href.startswith('/') else href

                if full_url not in seen_urls:
                    title = link.get_text(strip=True)
                    if len(title) > 10:
                        seen_urls.add(full_url)
                        unique_articles.append({
                            'url': full_url,
                            'title': title,
                            'link_elem': link
                        })

            print(f"   발견: {len(unique_articles)}개 기사")

            for article_info in unique_articles[:15]:
                try:
                    thumbnail = ''
                    parent = article_info['link_elem'].parent
                    if parent:
                        img = parent.find('img')
                        if not img and parent.parent:
                            img = parent.parent.find('img')

                        if img and img.get('src'):
                            src = img['src']
                            if src.startswith('/'):
                                thumbnail = base_url + src
                            elif src.startswith('http'):
                                thumbnail = src

                    content = self._fetch_content(article_info['url'])

                    article_data = {
                        'source': '치과신문',
                        'title': article_info['title'],
                        'url': article_info['url'],
                        'thumbnail': thumbnail,
                        'content': content,
                        'published_date': datetime.now().strftime('%Y-%m-%d'),
                        'category': '치과'
                    }

                    if self.db.insert_article(article_data):
                        new_articles += 1
                        print(f"   ✅ {article_info['title'][:40]}")

                    time.sleep(0.5)

                except Exception as e:
                    print(f"   ⚠️ 기사 처리 오류: {str(e)}")
                    continue

        except Exception as e:
            print(f"   ❌ 크롤링 오류: {str(e)}")

        return new_articles

    def crawl_dentalarirang(self):
        """덴탈아리랑 - 메인 페이지에서 최신 기사"""
        base_url = 'https://www.dentalarirang.com'
        main_url = base_url

        new_articles = 0

        try:
            response = requests.get(main_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')

            # 기사 링크 찾기
            all_links = soup.find_all('a', href=re.compile(r'/news/article'))

            seen_urls = set()
            unique_articles = []

            for link in all_links:
                href = link.get('href')
                full_url = base_url + href if href.startswith('/') else href

                if full_url not in seen_urls and 'articleView' in href:
                    title = link.get_text(strip=True)
                    if len(title) > 10:
                        seen_urls.add(full_url)
                        unique_articles.append({
                            'url': full_url,
                            'title': title,
                            'link_elem': link
                        })

            print(f"   발견: {len(unique_articles)}개 기사")

            for article_info in unique_articles[:15]:
                try:
                    thumbnail = ''
                    parent = article_info['link_elem'].parent
                    if parent:
                        img = parent.find('img')
                        if not img and parent.parent:
                            img = parent.parent.find('img')

                        if img and img.get('src'):
                            src = img['src']
                            if src.startswith('/'):
                                thumbnail = base_url + src
                            elif src.startswith('http'):
                                thumbnail = src

                    content = self._fetch_content(article_info['url'])

                    article_data = {
                        'source': '덴탈아리랑',
                        'title': article_info['title'],
                        'url': article_info['url'],
                        'thumbnail': thumbnail,
                        'content': content,
                        'published_date': datetime.now().strftime('%Y-%m-%d'),
                        'category': '치과'
                    }

                    if self.db.insert_article(article_data):
                        new_articles += 1
                        print(f"   ✅ {article_info['title'][:40]}")

                    time.sleep(0.5)

                except Exception as e:
                    print(f"   ⚠️ 기사 처리 오류: {str(e)}")
                    continue

        except Exception as e:
            print(f"   ❌ 크롤링 오류: {str(e)}")

        return new_articles

    def _fetch_content(self, url):
        """기사 본문 가져오기"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')

            # 본문 셀렉터 시도
            content_selectors = [
                '#article-view-content-div',
                'article .article-view-content-div',
                '.article-content',
                '.news-content',
                '.view-content',
                'div[itemprop="articleBody"]',
            ]

            for selector in content_selectors:
                content_tag = soup.select_one(selector)
                if content_tag:
                    for tag in content_tag.select('script, style, .ad, .related, .share'):
                        tag.decompose()

                    text = content_tag.get_text(strip=True)
                    if len(text) > 100:
                        return text[:2000]

        except:
            pass

        return ''


if __name__ == '__main__':
    crawler = DentalNewsCrawler()
    crawler.crawl_all()
