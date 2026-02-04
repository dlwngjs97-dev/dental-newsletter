#!/bin/bash
# 스케줄러 중지 스크립트

if [ -f ../logs/scheduler.pid ]; then
    PID=$(cat ../logs/scheduler.pid)
    echo "스케줄러 중지 중... (PID: $PID)"
    kill $PID
    rm ../logs/scheduler.pid
    echo "✅ 스케줄러가 중지되었습니다."
else
    echo "❌ 실행 중인 스케줄러가 없습니다."
fi
