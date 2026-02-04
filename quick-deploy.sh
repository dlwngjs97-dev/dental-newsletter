#!/bin/bash
# 빠른 배포 스크립트

echo "=== 치과 뉴스레터 배포 시작 ==="
echo ""

# 1. GitHub 저장소 확인
if git remote get-url origin > /dev/null 2>&1; then
    echo "✅ GitHub 저장소 연결됨: $(git remote get-url origin)"
else
    echo "⚠️  GitHub 저장소가 설정되지 않았습니다."
    echo ""
    echo "다음 명령어로 GitHub 저장소를 추가하세요:"
    echo "  git remote add origin https://github.com/[당신의_아이디]/dental-newsletter.git"
    echo ""
    read -p "GitHub 저장소 URL을 입력하세요 (또는 Enter로 건너뛰기): " repo_url

    if [ ! -z "$repo_url" ]; then
        git remote add origin "$repo_url"
        echo "✅ 저장소 추가 완료"
    else
        echo "❌ 저장소 설정 없이 종료합니다."
        exit 1
    fi
fi

echo ""
echo "2. 최신 변경사항 커밋 중..."
git add .

read -p "커밋 메시지 (Enter로 기본값 사용): " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Update: $(date '+%Y-%m-%d %H:%M')"
fi

if git diff --staged --quiet; then
    echo "변경사항 없음"
else
    git commit -m "$commit_msg"
    echo "✅ 커밋 완료"
fi

echo ""
echo "3. GitHub에 푸시 중..."
if git push -u origin main 2>&1; then
    echo "✅ GitHub 푸시 완료"
else
    echo "⚠️  푸시 실패. 다시 시도하세요."
    exit 1
fi

echo ""
echo "=== 배포 완료! ==="
echo ""
echo "다음 단계:"
echo "1. https://vercel.com 에서 로그인"
echo "2. 'New Project' 클릭"
echo "3. GitHub 저장소 'dental-newsletter' 선택"
echo "4. Root Directory: 'frontend' 입력"
echo "5. Deploy 클릭"
echo ""
echo "배포 완료 후 공유 가능한 URL을 받습니다:"
echo "  https://dental-newsletter-[고유코드].vercel.app"
echo ""
