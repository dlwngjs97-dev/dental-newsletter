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
        """치의신보"""
        base_url = 'https://www.dailydental.co.kr'
        main_url = base_url
        new_articles = 0

        try:
            response = requests.get(main_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')

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

                        # 썸네일 찾기 - 개선
                        thumbnail = ''

                        # 1. 링크의 부모/조상에서 img 찾기
                        current = link.parent
                        for _ in range(3):  # 3단계까지 탐색
                            if current:
                                imgs = current.find_all('img')
                                for img in imgs:
                                    src = img.get('src', '')
                                    if src and 'logo' not in src.lower() and 'icon' not in src.lower():
                                        if src.startswith('http'):
                                            thumbnail = src
                                        elif src.startswith('/'):
                                            # /www.example.com 형태 체크
                                            if src.startswith('//'):
                                                thumbnail = 'https:' + src
                                            elif base_url.replace('https://', '').replace('http://', '') in src:
                                                thumbnail = 'https:/' + src  # /www.example.com -> https://www.example.com
                                            else:
                                                thumbnail = base_url + src
                                        if thumbnail:
                                            break
                                if thumbnail:
                                    break
                                current = current.parent

                        unique_articles.append({
                            'url': full_url,
                            'title': title,
                            'thumbnail': thumbnail
                        })

            print(f"   발견: {len(unique_articles)}개 기사")

            for article_info in unique_articles[:15]:
                try:
                    # 기사 본문 가져오기 - 개선
                    content, article_img = self._fetch_content_with_image(article_info['url'], base_url)

                    # 썸네일이 없으면 본문에서 가져온 이미지 사용
                    final_thumbnail = article_info['thumbnail'] or article_img

                    article_data = {
                        'source': '치의신보',
                        'title': article_info['title'],
                        'url': article_info['url'],
                        'thumbnail': final_thumbnail,
                        'content': content,
                        'published_date': datetime.now().strftime('%Y-%m-%d'),
                        'category': '치과'
                    }

                    if self.db.insert_article(article_data):
                        new_articles += 1
                        print(f"   ✅ {article_info['title'][:40]}")

                    time.sleep(0.5)

                except Exception as e:
                    print(f"   ⚠️ {str(e)[:50]}")
                    continue

        except Exception as e:
            print(f"   ❌ {str(e)}")

        return new_articles

    def crawl_dentalnews(self):
        """치과신문"""
        base_url = 'https://www.dentalnews.or.kr'
        main_url = base_url
        new_articles = 0

        try:
            response = requests.get(main_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')

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

                        thumbnail = ''
                        current = link.parent
                        for _ in range(3):
                            if current:
                                imgs = current.find_all('img')
                                for img in imgs:
                                    src = img.get('src', '')
                                    if src and 'logo' not in src.lower() and 'icon' not in src.lower():
                                        if src.startswith('http'):
                                            thumbnail = src
                                        elif src.startswith('/'):
                                            if src.startswith('//'):
                                                thumbnail = 'https:' + src
                                            elif base_url.replace('https://', '').replace('http://', '') in src:
                                                thumbnail = 'https:/' + src
                                            else:
                                                thumbnail = base_url + src
                                        if thumbnail:
                                            break
                                if thumbnail:
                                    break
                                current = current.parent

                        unique_articles.append({
                            'url': full_url,
                            'title': title,
                            'thumbnail': thumbnail
                        })

            print(f"   발견: {len(unique_articles)}개 기사")

            for article_info in unique_articles[:15]:
                try:
                    content, article_img = self._fetch_content_with_image(article_info['url'], base_url)
                    final_thumbnail = article_info['thumbnail'] or article_img

                    article_data = {
                        'source': '치과신문',
                        'title': article_info['title'],
                        'url': article_info['url'],
                        'thumbnail': final_thumbnail,
                        'content': content,
                        'published_date': datetime.now().strftime('%Y-%m-%d'),
                        'category': '치과'
                    }

                    if self.db.insert_article(article_data):
                        new_articles += 1
                        print(f"   ✅ {article_info['title'][:40]}")

                    time.sleep(0.5)

                except Exception as e:
                    print(f"   ⚠️ {str(e)[:50]}")
                    continue

        except Exception as e:
            print(f"   ❌ {str(e)}")

        return new_articles

    def crawl_dentalarirang(self):
        """덴탈아리랑"""
        base_url = 'https://www.dentalarirang.com'
        main_url = base_url
        new_articles = 0

        try:
            response = requests.get(main_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')

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

                        thumbnail = ''
                        current = link.parent
                        for _ in range(3):
                            if current:
                                imgs = current.find_all('img')
                                for img in imgs:
                                    src = img.get('src', '')
                                    if src and 'logo' not in src.lower() and 'icon' not in src.lower():
                                        if src.startswith('http'):
                                            thumbnail = src
                                        elif src.startswith('/'):
                                            if src.startswith('//'):
                                                thumbnail = 'https:' + src
                                            elif base_url.replace('https://', '').replace('http://', '') in src:
                                                thumbnail = 'https:/' + src
                                            else:
                                                thumbnail = base_url + src
                                        if thumbnail:
                                            break
                                if thumbnail:
                                    break
                                current = current.parent

                        unique_articles.append({
                            'url': full_url,
                            'title': title,
                            'thumbnail': thumbnail
                        })

            print(f"   발견: {len(unique_articles)}개 기사")

            for article_info in unique_articles[:15]:
                try:
                    content, article_img = self._fetch_content_with_image(article_info['url'], base_url)
                    final_thumbnail = article_info['thumbnail'] or article_img

                    article_data = {
                        'source': '덴탈아리랑',
                        'title': article_info['title'],
                        'url': article_info['url'],
                        'thumbnail': final_thumbnail,
                        'content': content,
                        'published_date': datetime.now().strftime('%Y-%m-%d'),
                        'category': '치과'
                    }

                    if self.db.insert_article(article_data):
                        new_articles += 1
                        print(f"   ✅ {article_info['title'][:40]}")

                    time.sleep(0.5)

                except Exception as e:
                    print(f"   ⚠️ {str(e)[:50]}")
                    continue

        except Exception as e:
            print(f"   ❌ {str(e)}")

        return new_articles

    def _fetch_content_with_image(self, url, base_url):
        """기사 본문과 이미지 가져오기 - 개선"""
        content = ''
        image_url = ''

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')  # html.parser 사용

            # 본문 찾기 - 여러 패턴 시도
            content_found = False

            # 패턴 1: ID로 찾기 (news_body_area 추가)
            for content_id in ['news_body_area', 'article-view-content-div', 'articleBody', 'article_body']:
                content_tag = soup.find(id=content_id)
                if content_tag:
                    content_found = True
                    break

            # 패턴 2: 클래스로 찾기 (smartOutput 추가)
            if not content_found:
                for content_class in ['smartOutput', 'article-view-content-div', 'article-content', 'view-content', 'article_content']:
                    content_tag = soup.find('div', class_=content_class)
                    if content_tag:
                        content_found = True
                        break

            # 패턴 3: article 태그
            if not content_found:
                content_tag = soup.find('article')
                if content_tag:
                    content_found = True

            # 본문 추출
            if content_found and content_tag:
                # 불필요한 태그 제거
                for tag in content_tag.select('script, style, .ad, .related, .share, iframe'):
                    tag.decompose()

                # 이미지 찾기 (본문 내)
                imgs = content_tag.find_all('img')
                for img in imgs:
                    src = img.get('src', '')
                    if src and len(src) > 10 and 'logo' not in src.lower():
                        if src.startswith('http'):
                            image_url = src
                        elif src.startswith('/'):
                            if src.startswith('//'):
                                image_url = 'https:' + src
                            elif base_url.replace('https://', '').replace('http://', '') in src:
                                image_url = 'https:/' + src
                            else:
                                image_url = base_url + src
                        if image_url:
                            break

                # 텍스트 추출
                paragraphs = content_tag.find_all(['p', 'div'])
                text_parts = []

                for p in paragraphs:
                    text = p.get_text(strip=True)
                    if len(text) > 20:  # 의미있는 문장만
                        text_parts.append(text)

                if text_parts:
                    content = '\n\n'.join(text_parts[:10])  # 처음 10개 문단
                else:
                    # 전체 텍스트
                    content = content_tag.get_text(strip=True)

                # 길이 제한
                if len(content) > 3000:
                    content = content[:3000] + '...'

        except:
            pass

        return content, image_url


if __name__ == '__main__':
    crawler = DentalNewsCrawler()
    crawler.crawl_all()
