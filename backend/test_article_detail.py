#!/usr/bin/env python3
"""
기사 상세 페이지 구조 분석
"""
import requests
from bs4 import BeautifulSoup

# 샘플 기사 URL (각 언론사별)
test_urls = [
    ('치의신보', 'https://www.dailydental.co.kr/news/article.html?no=136544'),
    ('치과신문', 'https://www.dentalnews.or.kr/news/article.html?no=100062'),
    ('덴탈아리랑', 'https://www.dentalarirang.com/news/articleView.html?idxno=129613'),
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

for source, url in test_urls:
    print(f"\n{'='*80}")
    print(f"{source} - {url}")
    print('='*80)

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        # 썸네일 찾기
        print("\n[썸네일 찾기]")
        img_selectors = [
            'img[src*="news"]',
            'img[src*="article"]',
            '.article-image img',
            '.news-image img',
            'article img',
        ]

        for selector in img_selectors:
            imgs = soup.select(selector)
            if imgs:
                print(f"  {selector}: {len(imgs)}개 발견")
                for img in imgs[:3]:
                    src = img.get('src', '')
                    if len(src) > 20:
                        print(f"    - {src[:100]}")

        # 본문 찾기
        print("\n[본문 찾기]")
        content_selectors = [
            '#article-view-content-div',
            'div#article-view-content-div',
            '.article-view-content-div',
            'article',
            '.article-content',
            'div[itemprop="articleBody"]',
        ]

        for selector in content_selectors:
            content = soup.select_one(selector)
            if content:
                text = content.get_text(strip=True)
                if len(text) > 100:
                    print(f"  ✅ {selector}")
                    print(f"     길이: {len(text)}자")
                    print(f"     샘플: {text[:150]}...")
                    break

        # 날짜 찾기
        print("\n[날짜 찾기]")
        date_selectors = [
            'time',
            '.date',
            '.article-date',
            'span.date',
            'em',
        ]

        for selector in date_selectors:
            date_elem = soup.select_one(selector)
            if date_elem:
                date_text = date_elem.get_text(strip=True)
                if any(char.isdigit() for char in date_text):
                    print(f"  ✅ {selector}: {date_text}")
                    break

    except Exception as e:
        print(f"❌ 오류: {e}")
