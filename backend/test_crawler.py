#!/usr/bin/env python3
"""
사이트 구조 파악용 테스트 스크립트
"""
import requests
from bs4 import BeautifulSoup

def test_site(name, url):
    print(f"\n{'='*60}")
    print(f"테스트: {name}")
    print(f"URL: {url}")
    print('='*60)

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')

        # 다양한 셀렉터 시도
        selectors = [
            'article',
            '.article',
            '.news-item',
            '.list-item',
            'li.item',
            '.article-list li',
            '.news-list li',
            'div[class*="article"]',
            'div[class*="news"]',
        ]

        for selector in selectors:
            items = soup.select(selector)
            if len(items) > 0:
                print(f"\n✅ 발견: '{selector}' - {len(items)}개")

                # 첫 번째 아이템 분석
                if items:
                    first = items[0]
                    print(f"   첫 번째 아이템 구조:")

                    # 제목 찾기
                    title_selectors = ['a', '.title', 'h2', 'h3', 'h4', '.subject']
                    for ts in title_selectors:
                        title = first.select_one(ts)
                        if title:
                            print(f"   - 제목: {ts} → '{title.get_text(strip=True)[:50]}'")
                            break

                    # 링크 찾기
                    link = first.select_one('a')
                    if link and link.get('href'):
                        print(f"   - 링크: {link['href'][:80]}")

                    # 이미지 찾기
                    img = first.select_one('img')
                    if img and img.get('src'):
                        print(f"   - 이미지: {img['src'][:80]}")

                if len(items) >= 3:
                    break

    except Exception as e:
        print(f"❌ 오류: {e}")

# 각 사이트 테스트
sites = [
    ('치의신보', 'https://www.dailydental.co.kr/news/articleList.html?sc_section_code=S1N1'),
    ('치과신문', 'https://www.dentalnews.or.kr/news/articleList.html?sc_section_code=S1N1'),
    ('덴탈아리랑', 'https://www.dentalarirang.com/news/articleList.html?sc_section_code=S1N1'),
]

for name, url in sites:
    test_site(name, url)

print(f"\n{'='*60}")
print("테스트 완료")
print('='*60)
