import schedule
import time
from datetime import datetime
from crawler import DentalNewsCrawler

def scheduled_crawl():
    """매일 크롤링 실행"""
    print(f"\n{'='*50}")
    print(f"예약된 크롤링 시작: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")

    crawler = DentalNewsCrawler()
    crawler.crawl_all()

def run_scheduler():
    """스케줄러 실행"""
    # 매일 오전 10시에 크롤링
    schedule.every().day.at("10:00").do(scheduled_crawl)

    print("=== 치과 뉴스레터 스케줄러 시작 ===")
    print("크롤링 예약: 매일 10:00")
    print("첫 크롤링을 바로 실행합니다...\n")

    # 시작 시 즉시 한 번 실행
    scheduled_crawl()

    # 스케줄 대기
    while True:
        schedule.run_pending()
        time.sleep(60)  # 1분마다 체크


if __name__ == '__main__':
    run_scheduler()
