# 치과 뉴스레터

치의신보, 치과신문, 덴탈아리랑의 최신 뉴스를 한곳에서 확인할 수 있는 웹사이트

---

## 주요 기능

- ✅ 3개 주요 치과 언론사 뉴스 자동 크롤링
- ✅ 세련된 카드 형태 UI
- ✅ 언론사별 필터링
- ✅ 실시간 검색
- ✅ 반응형 디자인 (모바일/태블릿/PC)
- ✅ 매일 자동 업데이트 (09:00, 18:00)

---

## 시스템 구조

```
dental-newsletter/
├── backend/              # Python 크롤러
│   ├── crawler.py        # 뉴스 크롤링 엔진
│   ├── database.py       # SQLite 데이터베이스
│   ├── scheduler.py      # 자동 스케줄러
│   └── run_once.py       # 1회 실행 스크립트
├── frontend/             # Next.js 웹사이트
│   ├── app/              # 페이지
│   ├── components/       # React 컴포넌트
│   └── public/           # 정적 파일
└── data/                 # 크롤링 데이터
    ├── articles.db       # SQLite DB
    └── articles.json     # JSON 내보내기
```

---

## 설치 및 실행

### 1단계: 백엔드 설정

```bash
cd dental-newsletter/backend

# Python 패키지 설치
pip install -r requirements.txt

# 1회 크롤링 실행 (테스트)
python run_once.py
```

### 2단계: 프론트엔드 설정

```bash
cd dental-newsletter/frontend

# npm 패키지 설치
npm install

# 개발 서버 실행
npm run dev
```

웹사이트가 `http://localhost:3000`에서 실행됩니다.

### 3단계: 자동 스케줄러 실행 (선택사항)

매일 자동으로 크롤링하려면:

```bash
cd dental-newsletter/backend

# 스케줄러 실행 (백그라운드)
nohup python scheduler.py > scheduler.log 2>&1 &
```

---

## 크롤링 일정

- **매일 오전 9시**: 첫 번째 크롤링
- **매일 오후 6시**: 두 번째 크롤링

---

## 배포 (프로덕션)

### Vercel 배포 (프론트엔드)

```bash
cd frontend
npm run build
vercel deploy
```

### AWS/서버 배포 (백엔드)

```bash
# 서버에 접속 후
cd dental-newsletter/backend

# cron 등록 (매일 09:00, 18:00)
crontab -e

# 추가:
0 9 * * * cd /path/to/dental-newsletter/backend && python run_once.py
0 18 * * * cd /path/to/dental-newsletter/backend && python run_once.py
```

---

## 주의사항

⚠️ **법적 리스크**
- 이 프로젝트는 뉴스 기사 전문을 크롤링합니다
- 저작권 문제가 발생할 수 있습니다
- 상업적 사용 시 각 언론사와 협의 필요

⚠️ **robots.txt 준수**
- 크롤링 전 각 사이트의 robots.txt 확인 권장
- 과도한 요청으로 서버에 부하를 주지 않도록 주의

---

## 기술 스택

**백엔드**
- Python 3.9+
- BeautifulSoup4 (HTML 파싱)
- SQLite (데이터 저장)
- Schedule (자동화)

**프론트엔드**
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS

---

## 개발자

치과 뉴스레터 v1.0.0

---

## 라이선스

개인 프로젝트 - 상업적 사용 시 법적 검토 필수
