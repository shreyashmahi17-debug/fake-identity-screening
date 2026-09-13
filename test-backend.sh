#!/bin/bash

# Backend Connection Test Script
# This script tests if the backend is reachable and responding

BACKEND_URL="https://fake-identity-screening.onrender.com"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 Testing Backend Connection"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "📍 Backend URL: $BACKEND_URL"
echo ""

# Test 1: Root endpoint
echo "1️⃣  Testing root endpoint (GET /)..."
RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" "$BACKEND_URL/")
HTTP_CODE=$(echo "$RESPONSE" | grep "HTTP_CODE:" | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed '/HTTP_CODE:/d')

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Root endpoint working!"
    echo "Response: $BODY"
else
    echo "❌ Root endpoint failed (HTTP $HTTP_CODE)"
    echo "Response: $BODY"
fi
echo ""

# Test 2: Health endpoint
echo "2️⃣  Testing health endpoint (GET /health)..."
RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" "$BACKEND_URL/health")
HTTP_CODE=$(echo "$RESPONSE" | grep "HTTP_CODE:" | cut -d':' -f2)
BODY=$(echo "$RESPONSE" | sed '/HTTP_CODE:/d')

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Health endpoint working!"
    echo "Response: $BODY"
else
    echo "❌ Health endpoint failed (HTTP $HTTP_CODE)"
    echo "Response: $BODY"
fi
echo ""

# Test 3: CORS preflight
echo "3️⃣  Testing CORS preflight (OPTIONS /ocr)..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X OPTIONS \
    -H "Origin: https://your-app.vercel.app" \
    -H "Access-Control-Request-Method: POST" \
    -H "Access-Control-Request-Headers: Content-Type" \
    "$BACKEND_URL/ocr")

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ CORS preflight working!"
else
    echo "❌ CORS preflight failed (HTTP $HTTP_CODE)"
fi
echo ""

# Test 4: Response time
echo "4️⃣  Testing response time..."
START=$(date +%s)
curl -s "$BACKEND_URL/" > /dev/null
END=$(date +%s)
DIFF=$((END - START))

if [ $DIFF -lt 5 ]; then
    echo "✅ Response time: ${DIFF}s (Backend is warm)"
elif [ $DIFF -lt 30 ]; then
    echo "⚠️  Response time: ${DIFF}s (Backend might be waking up)"
else
    echo "🐌 Response time: ${DIFF}s (Cold start detected)"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Test Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "If all tests passed, your backend is ready for Vercel frontend!"
echo ""
echo "Next steps:"
echo "1. Deploy frontend to Vercel: cd frontend && vercel --prod"
echo "2. Set environment variable in Vercel: VITE_API_URL=$BACKEND_URL"
echo "3. Test the full application"
echo ""
