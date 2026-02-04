#!/bin/bash
# 치과 뉴스레터 크롤러 배포 스크립트

echo "=== 치과 뉴스레터 크롤러 배포 ==="

# 1. 의존성 설치
echo "1. 의존성 설치 중..."
pip3 install -r requirements.txt

# 2. 데이터 디렉토리 생성
echo "2. 데이터 디렉토리 확인..."
mkdir -p ../data
mkdir -p ../frontend/public/data

# 3. 초기 크롤링 실행
echo "3. 초기 크롤링 실행..."
python3 crawler.py

# 4. JSON 파일 프론트엔드에 복사
echo "4. JSON 파일 복사..."
cp ../data/articles.json ../frontend/public/data/

# 5. 스케줄러를 백그라운드에서 실행
echo "5. 스케줄러 시작..."
nohup python3 scheduler.py > ../logs/scheduler.log 2>&1 &
echo $! > ../logs/scheduler.pid

echo ""
echo "✅ 배포 완료!"
echo "   - 스케줄러: 매일 오전 10시 실행"
echo "   - PID: $(cat ../logs/scheduler.pid)"
echo "   - 로그: $(pwd)/../logs/scheduler.log"
echo ""
echo "스케줄러 중지: kill \$(cat $(pwd)/../logs/scheduler.pid)"
