#!/bin/bash
# 认证系统 API 集成测试：注册→合并→登出→登录→持久化
set -e
cd /home/z/my-project
JAR=scripts/test-cookies.txt
BASE=http://localhost:3000
PASS=0; FAILED=0

check() { # $1=描述 $2=期望包含的字符串 $3=实际值
  if echo "$3" | grep -q "$2"; then PASS=$((PASS+1)); echo "✓ $1";
  else FAILED=$((FAILED+1)); echo "✗ $1 — 期望含 [$2]，实际: $(echo "$3" | head -c 300)"; fi
}

rm -f "$JAR"

echo "== 1. 未登录状态 =="
R=$(curl -s $BASE/api/auth/me)
check "me 返回访客(未登录)" '"user":null' "$R"

echo "== 2. 访客先做一题（作为待合并数据） =="
R=$(curl -s -X POST $BASE/api/progress -H 'Content-Type: application/json' \
  -d '{"questionId":"2009-ds-01","userAnswer":"A","isCorrect":true,"mode":"practice"}')
check "访客提交作答" '"ok":true' "$R"

echo "== 3. 注册（应自动登录并合并访客数据） =="
R=$(curl -s -c "$JAR" -X POST $BASE/api/auth/register -H 'Content-Type: application/json' \
  -d '{"name":"tester_x","password":"pass123"}')
check "注册成功" '"ok":true' "$R"

R=$(curl -s -b "$JAR" $BASE/api/auth/me)
check "注册后 me 已登录" 'tester_x' "$R"

R=$(curl -s -b "$JAR" $BASE/api/progress)
check "访客作答已并入账号(attempted>=1)" '"attempted":1' "$R"

echo "== 4. 重复注册应被拒绝 =="
R=$(curl -s -X POST $BASE/api/auth/register -H 'Content-Type: application/json' \
  -d '{"name":"tester_x","password":"pass123"}')
check "重名注册被拒" '已被注册' "$R"

R=$(curl -s -X POST $BASE/api/auth/register -H 'Content-Type: application/json' \
  -d '{"name":"a","password":"pass123"}')
check "过短用户名被拒" '用户名需' "$R"

echo "== 5. 登出 =="
R=$(curl -s -b "$JAR" -c "$JAR" -X POST $BASE/api/auth/logout)
check "登出成功" '"ok":true' "$R"
R=$(curl -s -b "$JAR" $BASE/api/auth/me)
check "登出后 me 为访客" '"user":null' "$R"

echo "== 6. 错误密码登录被拒 =="
R=$(curl -s -X POST $BASE/api/auth/login -H 'Content-Type: application/json' \
  -d '{"name":"tester_x","password":"wrong!"}')
check "错误密码被拒" '用户名或密码错误' "$R"

echo "== 7. 登录（持久化验证：记录仍在账号下） =="
R=$(curl -s -c "$JAR" -X POST $BASE/api/auth/login -H 'Content-Type: application/json' \
  -d '{"name":"tester_x","password":"pass123"}')
check "登录成功" '"ok":true' "$R"
R=$(curl -s -b "$JAR" $BASE/api/progress)
check "登录后记录持久存在" '"attempted":1' "$R"

echo "== 8. 登录状态下做题写入账号 =="
R=$(curl -s -b "$JAR" -X POST $BASE/api/progress -H 'Content-Type: application/json' \
  -d '{"questionId":"2009-ds-02","userAnswer":"B","isCorrect":false,"mode":"practice"}')
check "登录状态作答" '"ok":true' "$R"
R=$(curl -s -b "$JAR" $BASE/api/progress)
check "账号记录累计2题" '"attempted":2' "$R"
R=$(curl -s $BASE/api/progress)
check "访客视角为空（数据已隔离）" '"attempted":0' "$R"

echo ""
echo "========== 结果: $PASS 通过 / $FAILED 失败 =="
rm -f "$JAR"
[ $FAILED -eq 0 ]
