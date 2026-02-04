# 치과 뉴스레터 배포 가이드

## 📦 배포 방법 (Vercel + GitHub)

### 1단계: GitHub에 저장소 생성 및 푸시

```bash
# 1. GitHub에 새 저장소 생성
# https://github.com/new 에서 'dental-newsletter' 저장소 생성
# (Private 또는 Public 선택)

# 2. 로컬 저장소에 원격 저장소 추가
cd /Users/ijuheon/dental-newsletter
git remote add origin https://github.com/[당신의_아이디]/dental-newsletter.git

# 3. 푸시
git branch -M main
git push -u origin main
```

### 2단계: Vercel 배포

#### 방법 A: Vercel 웹사이트 (추천)

1. [Vercel](https://vercel.com) 가입/로그인
2. "Add New Project" 클릭
3. GitHub 저장소 연결
4. `dental-newsletter` 저장소 선택
5. **Root Directory 설정:** `frontend` 입력
6. "Deploy" 클릭

#### 방법 B: Vercel CLI

```bash
# 1. Vercel CLI 설치
npm install -g vercel

# 2. 로그인
vercel login

# 3. frontend 폴더에서 배포
cd frontend
vercel

# 4. 프로덕션 배포
vercel --prod
```

### 3단계: 자동 크롤링 설정

GitHub Actions가 이미 설정되어 있어 다음과 같이 작동합니다:

✅ **매일 오전 10시 (한국시간)** 자동 크롤링
✅ 새 기사를 자동으로 커밋 & 푸시
✅ Vercel이 자동으로 재배포

**수동 크롤링 실행:**
1. GitHub 저장소 → "Actions" 탭
2. "Daily News Crawling" 워크플로우 선택
3. "Run workflow" 클릭

---

## 🌐 배포 후 URL

배포가 완료되면 다음과 같은 URL을 받습니다:

```
https://dental-newsletter-[고유코드].vercel.app
```

**커스텀 도메인 설정 (선택사항):**
1. Vercel 프로젝트 → Settings → Domains
2. 도메인 입력 및 DNS 설정

---

## 🔧 환경 변수 (필요시)

Vercel 프로젝트 설정에서 환경 변수 추가:

```
# 예시
API_KEY=your_api_key
DATABASE_URL=your_database_url
```

---

## 📊 모니터링

### Vercel 대시보드
- 배포 상태 확인
- 로그 확인
- 트래픽 통계

### GitHub Actions
- 크롤링 실행 기록
- 에러 로그 확인

---

## 🚨 문제 해결

### 배포 실패 시

1. **빌드 로그 확인**
   - Vercel 대시보드 → Deployments → 실패한 배포 → Logs

2. **로컬에서 빌드 테스트**
   ```bash
   cd frontend
   npm run build
   ```

3. **Node 버전 확인**
   - `package.json`에 engines 추가:
   ```json
   "engines": {
     "node": ">=18.0.0"
   }
   ```

### 크롤링 실패 시

1. **GitHub Actions 로그 확인**
   - GitHub 저장소 → Actions → 실패한 워크플로우 클릭

2. **수동 크롤링 테스트**
   ```bash
   cd backend
   python3 crawler.py
   ```

---

## 📱 공유하기

배포 완료 후:

```
https://dental-newsletter-[고유코드].vercel.app
```

이 URL을 복사하여 공유하세요!

---

## 💡 팁

1. **빠른 배포:** Git push만 하면 자동 배포
2. **무료 플랜:** Vercel 무료 플랜으로 충분
3. **커스텀 도메인:** 나만의 도메인 연결 가능
4. **HTTPS 자동:** Vercel이 자동으로 SSL 인증서 발급
