# 치과 뉴스레터 사용 가이드

## 빠른 시작

### 1. 프론트엔드 실행

```bash
cd /Users/ijuheon/dental-newsletter/frontend
npm run dev
```

웹사이트가 **http://localhost:3000**에서 실행됩니다.

---

## 크롤러 개선 가이드

현재 크롤러는 0개의 기사를 수집했습니다.
각 사이트의 **실제 HTML 구조**를 파악해서 CSS 셀렉터를 수정해야 합니다.

### 크롤러 수정 방법

1. **브라우저에서 각 사이트 접속**
   - 치의신보: https://www.dailydental.co.kr/
   - 치과신문: https://www.dentalnews.or.kr/
   - 덴탈아리랑: https://www.dentalarirang.com/

2. **개발자 도구 열기** (F12 또는 우클릭 > 검사)

3. **기사 목록의 HTML 구조 확인**
   - 기사 제목이 어떤 태그에 있는지
   - 링크는 어떤 속성에 있는지
   - 썸네일 이미지는 어디 있는지
   - 날짜는 어떤 형식인지

4. **`backend/crawler.py` 수정**

예시:
```python
# 현재 (작동 안 함)
articles = soup.select('.article-list .article-list-content li')

# 실제 사이트에 맞게 수정 (예시)
articles = soup.select('.news-list .item')  # 실제 클래스명으로 변경
```

5. **테스트**
```bash
cd backend
python3 run_once.py
```

---

## 자동화 설정

### 매일 자동 크롤링 (cron)

```bash
# crontab 편집
crontab -e

# 추가 (매일 오전 9시, 오후 6시)
0 9 * * * cd /Users/ijuheon/dental-newsletter/backend && /usr/bin/python3 run_once.py >> /Users/ijuheon/dental-newsletter/logs/crawler.log 2>&1
0 18 * * * cd /Users/ijuheon/dental-newsletter/backend && /usr/bin/python3 run_once.py >> /Users/ijuheon/dental-newsletter/logs/crawler.log 2>&1
```

또는 **스케줄러 사용**:
```bash
cd backend
python3 scheduler.py
```

---

## 현재 상태

✅ 프론트엔드: 완성 (세련된 UI, 필터링, 검색)
✅ 백엔드: 구조 완성 (DB, 크롤러, 스케줄러)
⚠️ 크롤러: HTML 셀렉터 수정 필요

**샘플 데이터**로 UI를 먼저 확인할 수 있습니다.

---

## 배포 옵션

### Vercel (프론트엔드)
```bash
cd frontend
npm run build
vercel deploy
```

### 백엔드 서버
- AWS EC2, DigitalOcean, 또는 개인 서버
- cron으로 자동 크롤링
- JSON 파일을 Vercel에 업로드하거나 API로 제공

---

## 법적 주의사항

⚠️ **중요**: 이 프로젝트는 뉴스 기사 전문을 크롤링합니다.

- 저작권법 위반 가능성
- 각 언론사의 이용 약관 확인 필요
- 상업적 사용 시 반드시 제휴 계약 필요

**권장 대안**:
1. RSS 피드만 사용 (제목 + 링크)
2. 언론사와 정식 제휴
3. 개인 학습용으로만 사용

---

## 문제 해결

### 크롤링 0개 수집
- `backend/crawler.py`의 CSS 셀렉터 수정
- 각 사이트 HTML 구조 확인

### 프론트엔드 빌드 오류
```bash
cd frontend
rm -rf .next node_modules
npm install
npm run dev
```

### 포트 충돌
```bash
# 다른 포트 사용
npm run dev -- -p 3001
```

---

## 다음 단계

1. **크롤러 수정** → 실제 기사 수집
2. **프론트엔드 확인** → UI/UX 개선
3. **자동화 설정** → cron 또는 스케줄러
4. **배포** → Vercel + 서버

확인 부탁드립니다!
