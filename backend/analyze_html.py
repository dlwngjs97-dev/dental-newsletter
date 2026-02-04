#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

url = 'https://www.dentalarirang.com/news/articleList.html?sc_section_code=S1N1'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

response = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(response.text, 'lxml')

# section-list 찾기
section_list = soup.select('.section-list')
print(f"section-list: {len(section_list)}개 발견\n")

if section_list:
    # 첫 번째 section-list의 ul 찾기
    ul = section_list[0].select_one('ul')
    if ul:
        items = ul.select('li')
        print(f"리스트 아이템: {len(items)}개\n")

        if items:
            first = items[0]
            print("첫 번째 기사 구조:")
            print("-" * 60)

            # 썸네일
            thumb = first.select_one('.list-img img')
            if thumb:
                print(f"썸네일: {thumb.get('src', '')}")

            # 제목
            title = first.select_one('.list-titles a')
            if title:
                print(f"제목: {title.get_text(strip=True)}")
                print(f"링크: {title.get('href', '')}")

            # 날짜
            date = first.select_one('.list-dated')
            if date:
                print(f"날짜: {date.get_text(strip=True)}")

            # 전체 HTML (일부)
            print("\nHTML 구조 (일부):")
            print(str(first)[:500])
