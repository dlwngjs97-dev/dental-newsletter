#!/usr/bin/env python3
"""
실제 사이트 HTML 구조 상세 분석
"""
import requests
from bs4 import BeautifulSoup

def analyze_site(name, url):
    print(f"\n{'='*80}")
    print(f"{name} 분석")
    print(f"URL: {url}")
    print('='*80)

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')

        # HTML 전체 구조 출력 (처음 3000자)
        print("\n[HTML 구조 샘플]")
        print(response.text[:3000])
        print("\n...")

        # 모든 li 태그 찾기
        all_li = soup.find_all('li', limit=20)
        print(f"\n[발견된 li 태그: {len(all_li)}개]")

        for i, li in enumerate(all_li[:5], 1):
            print(f"\nLI {i}:")
            print(f"  Class: {li.get('class', [])}")
            print(f"  내용: {li.get_text(strip=True)[:100]}")

            # a 태그 찾기
            a_tags = li.find_all('a', limit=3)
            for a in a_tags:
                print(f"    링크: {a.get('href', '')} -> {a.get_text(strip=True)[:50]}")

            # img 태그 찾기
            img = li.find('img')
            if img:
                print(f"    이미지: {img.get('src', '')[:80]}")

    except Exception as e:
        print(f"\n❌ 오류: {e}")

# 테스트
sites = [
    ('치의신보', 'https://www.dailydental.co.kr/news/articleList.html?sc_section_code=S1N1'),
    ('치과신문', 'https://www.dentalnews.or.kr/news/articleList.html?sc_section_code=S1N1'),
    ('덴탈아리랑', 'https://www.dentalarirang.com/news/articleList.html?sc_section_code=S1N1'),
]

for name, url in sites:
    analyze_site(name, url)
    print("\n" + "="*80)
