# 치과 뉴스레터 크롤러 배포 가이드

## 옵션 1: 간단한 백그라운드 실행 (추천)

```bash
cd /Users/ijuheon/dental-newsletter/backend

# 배포 (스케줄러 시작)
chmod +x deploy.sh stop.sh
./deploy.sh

# 스케줄러 중지
./stop.sh

# 로그 확인
tail -f ../logs/scheduler.log
```

**특징:**
- 간단하고 빠른 설정
- 수동으로 시작/중지 가능
- 터미널 종료 후에도 실행 유지
- 시스템 재부팅 시 수동으로 재시작 필요

---

## 옵션 2: macOS launchd (시스템 재부팅 후에도 자동 실행)

```bash
cd /Users/ijuheon/dental-newsletter/backend

# 1. 로그 디렉토리 생성
mkdir -p ../logs

# 2. plist 파일 설치
cp com.dental.newsletter.plist ~/Library/LaunchAgents/

# 3. launchd에 등록 및 시작
launchctl load ~/Library/LaunchAgents/com.dental.newsletter.plist

# 4. 상태 확인
launchctl list | grep dental

# 5. 중지
launchctl unload ~/Library/LaunchAgents/com.dental.newsletter.plist

# 6. 로그 확인
tail -f /Users/ijuheon/dental-newsletter/logs/scheduler.log
```

**특징:**
- 시스템 재부팅 후에도 자동 실행
- 프로세스가 죽으면 자동 재시작
- macOS 시스템 서비스로 관리
- 설정이 약간 복잡

---

## 크롤링 스케줄

**실행 시간:** 매일 오전 10시
**수집 대상:**
- 치의신보 (15개 기사)
- 치과신문 (15개 기사)
- 덴탈아리랑 (15개 기사)

**데이터 저장 위치:**
- `/Users/ijuheon/dental-newsletter/data/articles.json`
- `/Users/ijuheon/dental-newsletter/frontend/public/data/articles.json`

---

## 문제 해결

### 스케줄러가 실행되지 않을 때
```bash
# 프로세스 확인
ps aux | grep scheduler.py

# PID 파일 확인
cat /Users/ijuheon/dental-newsletter/logs/scheduler.pid

# 로그 확인
tail -f /Users/ijuheon/dental-newsletter/logs/scheduler.log
```

### Python 경로 확인
```bash
which python3
# 결과를 com.dental.newsletter.plist의 python3 경로에 맞춰주세요
```

### 수동 크롤링 실행
```bash
cd /Users/ijuheon/dental-newsletter/backend
python3 crawler.py
```
