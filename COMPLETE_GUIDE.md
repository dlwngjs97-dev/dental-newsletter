# 치과 뉴스레터 - 완성 가이드

## ✅ 완성된 기능

### 프론트엔드 (100%)
- 🎨 **메인 페이지**: 세련된 카드 형태, 필터링, 검색
- 📄 **상세 페이지**: 썸네일, 본문, 원문 보기 버튼
- 📱 **반응형 디자인**: 모바일/태블릿/PC
- 🔍 **실시간 검색**: 제목/내용 검색
- 🏷️ **언론사 필터**: 전체/치의신보/치과신문/덴탈아리랑

### 백엔드
- 🤖 **크롤러**: 구조 완성 (사이트별 조정 필요)
- 💾 **데이터베이스**: SQLite
- ⏰ **스케줄러**: 자동 크롤링

---

## 🚀 실행 방법

```bash
cd /Users/ijuheon/dental-newsletter/frontend
npm run dev
```

**http://localhost:3000** 접속

---

## 📸 주요 기능

### 1. 메인 페이지
- 기사 카드 클릭 → **상세 페이지**로 이동
- 언론사별 필터링
- 실시간 검색

### 2. 상세 페이지
- 📰 썸네일 이미지
- 📝 기사 전문 표시
- 🔗 **"원문 보기"** 버튼 → 해당 언론사 사이트로 이동
- ← 목록으로 돌아가기

---

## 🔧 크롤러 개선 방법

현재 샘플 데이터로 작동 중입니다.
실제 기사를 수집하려면 **각 사이트의 HTML 구조**를 확인해야 합니다.

### 단계별 가이드

#### 1. 브라우저에서 사이트 열기
```
- 치의신보: https://www.dailydental.co.kr/
- 치과신문: https://www.dentalnews.or.kr/
- 덴탈아리랑: https://www.dentalarirang.com/
```

#### 2. 개발자 도구 (F12)
- Elements 탭 열기
- 기사 목록 영역 찾기

#### 3. CSS 셀렉터 확인
찾아야 할 것:
- 기사 목록 컨테이너 (예: `.article-list`)
- 각 기사 아이템 (예: `li.article-item`)
- 제목 링크 (예: `.title a`)
- 썸네일 이미지 (예: `.thumb img`)
- 날짜 (예: `.date`)

#### 4. `backend/crawler_improved.py` 수정

```python
# 예시: 실제 HTML 구조에 맞게 수정
selectors = [
    'ul.실제클래스명 li',  # 실제 발견한 셀렉터로 변경
    '.article-list li',
    # ... 추가
]
```

#### 5. 테스트
```bash
cd backend
python3 crawler_improved.py
```

---

## 📁 파일 구조

```
dental-newsletter/
├── backend/
│   ├── crawler_improved.py    # ✅ 개선된 크롤러
│   ├── database.py            # DB 관리
│   └── run_once.py            # 1회 실행
├── frontend/
│   ├── app/
│   │   ├── page.tsx           # 메인 페이지
│   │   └── article/[id]/      # ✅ 상세 페이지
│   │       └── page.tsx
│   └── components/
│       ├── ArticleCard.tsx    # ✅ 수정됨 (상세 페이지 링크)
│       ├── FilterBar.tsx
│       └── Header.tsx
└── data/
    └── articles.json          # ✅ 샘플 데이터 (썸네일 포함)
```

---

## 🎯 다음 단계

### 즉시 사용 가능
- ✅ UI 확인
- ✅ 상세 페이지 테스트
- ✅ 필터링/검색 테스트

### 크롤러 개선 (선택)
1. 각 사이트 HTML 구조 확인
2. `crawler_improved.py` 셀렉터 수정
3. 테스트 실행

### 배포 (선택)
- **Vercel**: 프론트엔드 무료 배포
- **서버**: 크롤러 자동화 (cron)

---

## 💡 팁

### 썸네일 표시
- 현재 샘플 데이터는 Unsplash 이미지 사용
- 실제 크롤링 시 각 사이트의 썸네일 수집

### 본문 내용
- 샘플 데이터는 전체 본문 포함
- 실제 크롤링 시 각 사이트에서 본문 추출

### 원문 보기 버튼
- 상세 페이지 하단에 위치
- 해당 언론사 사이트로 새 탭 이동

---

## ⚠️ 법적 주의사항

**현재는 샘플 데이터로 작동**하므로 법적 문제 없음.

실제 크롤링 시:
- 저작권법 검토 필요
- 각 언론사 이용 약관 확인
- 상업적 사용 시 제휴 필요

---

## 🆘 문제 해결

### 포트 충돌
```bash
npm run dev -- -p 3001
```

### 빌드 에러
```bash
rm -rf .next node_modules
npm install
npm run dev
```

### 크롤러 0개 수집
- HTML 구조 확인 필요
- 셀렉터 수정 필요

---

**완성되었습니다!**
http://localhost:3000 에서 확인하세요.
