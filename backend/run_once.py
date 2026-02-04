#!/usr/bin/env python3
"""
치과 뉴스레터 - 1회 실행 스크립트
크롤링 한 번 실행 후 JSON 파일을 프론트엔드로 복사
"""

import shutil
from pathlib import Path
from crawler import DentalNewsCrawler

def main():
    print("=== 치과 뉴스레터 1회 크롤링 시작 ===\n")

    # 크롤링 실행
    crawler = DentalNewsCrawler()
    crawler.crawl_all()

    # JSON 파일을 프론트엔드 public 폴더로 복사
    source = Path(__file__).parent / '../data/articles.json'
    destination = Path(__file__).parent / '../frontend/public/data/articles.json'

    # 디렉토리 생성
    destination.parent.mkdir(parents=True, exist_ok=True)

    # 파일 복사
    if source.exists():
        shutil.copy2(source, destination)
        print(f"\n✅ JSON 파일 복사 완료: {destination}")
    else:
        print(f"\n⚠️ JSON 파일이 없습니다: {source}")

    print("\n=== 크롤링 완료 ===")
    print("프론트엔드를 실행하세요:")
    print("  cd frontend")
    print("  npm install")
    print("  npm run dev")

if __name__ == '__main__':
    main()
