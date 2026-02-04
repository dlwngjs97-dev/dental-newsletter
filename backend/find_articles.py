#!/usr/bin/env python3
"""
기사 링크 패턴 찾기 - 공격적 분석
"""
import requests
from bs4 import BeautifulSoup
import re

def find_article_links(name, url):
    print(f"\n{'='*80}")
    print(f"{name} - 기사 링크 찾기")
    print('='*80)

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'lxml')

        # 모든 a 태그 중 기사 링크로 보이는 것들 찾기
        all_links = soup.find_all('a', href=True)

        # 기사 링크 패턴 (articleView 포함)
        article_pattern = re.compile(r'article.*View', re.IGNORECASE)

        article_links = []
        for link in all_links:
            href = link.get('href', '')
            text = link.get_text(strip=True)

            # 기사 링크로 판단되는 조건
            if article_pattern.search(href) and len(text) > 10 and len(text) < 200:
                article_links.append({
                    'href': href,
                    'text': text,
                    'parent_class': link.parent.get('class', []) if link.parent else []
                })

        print(f"\n✅ 발견된 기사 링크: {len(article_links)}개")

        if article_links:
            print("\n[처음 5개 기사]")
            for i, article in enumerate(article_links[:5], 1):
                print(f"\n{i}. 제목: {article['text'][:60]}")
                print(f"   링크: {article['href'][:80]}")
                print(f"   부모 클래스: {article['parent_class']}")

            # 공통 패턴 찾기
            if len(article_links) > 0:
                first_parent = article_links[0]['parent_class']
                print(f"\n📌 추천 셀렉터:")

                # 부모의 부모 찾기
                first_link = soup.find('a', href=article_links[0]['href'])
                if first_link and first_link.parent and first_link.parent.parent:
                    container = first_link.parent.parent
                    print(f"   컨테이너 태그: {container.name}")
                    print(f"   컨테이너 클래스: {container.get('class', [])}")

                    if container.name == 'ul':
                        print(f"\n   ✅ 사용할 셀렉터:")
                        if container.get('class'):
                            class_name = ' '.join(container.get('class'))
                            print(f"      'ul.{class_name.replace(' ', '.')} > li'")
                        else:
                            print(f"      특정 컨테이너 아래 ul > li")

        else:
            print("\n⚠️ 기사 링크를 찾을 수 없습니다")

            # 다른 패턴 시도
            print("\n[대안: 'news' 또는 'article' 포함 링크]")
            alternative_links = [a for a in all_links if ('news' in a.get('href', '').lower() or 'article' in a.get('href', '').lower()) and len(a.get_text(strip=True)) > 10]

            for i, link in enumerate(alternative_links[:5], 1):
                print(f"{i}. {link.get_text(strip=True)[:50]} -> {link.get('href', '')[:60]}")

    except Exception as e:
        print(f"\n❌ 오류: {e}")

# 각 사이트 분석
sites = [
    ('치의신보', 'https://www.dailydental.co.kr/news/articleList.html?sc_section_code=S1N1'),
    ('치과신문', 'https://www.dentalnews.or.kr/news/articleList.html?sc_section_code=S1N1'),
    ('덴탈아리랑', 'https://www.dentalarirang.com/news/articleList.html?sc_section_code=S1N1'),
]

for name, url in sites:
    find_article_links(name, url)

print("\n" + "="*80)
print("분석 완료")
print("="*80)
