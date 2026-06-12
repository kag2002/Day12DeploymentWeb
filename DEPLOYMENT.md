# Deployment Information

## Public URL
https://chatbotsearchweb-production.up.railway.app

## Platform
Railway

## Test Commands

### 1. Health Check
```bash
curl https://chatbotsearchweb-production.up.railway.app/health
# Expected: {"status": "ok", ...}
```

### 2. Readiness Check
```bash
curl https://chatbotsearchweb-production.up.railway.app/ready
# Expected: {"ready": true}
```

### 3. API Test (Without authentication)
```bash
curl -X POST https://chatbotsearchweb-production.up.railway.app/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello"}'
# Expected response: 401 Unauthorized (detail: "Invalid or missing API key")
```

### 4. API Test (With authentication)
```bash
curl -X POST https://chatbotsearchweb-production.up.railway.app/ask \
  -H "X-API-Key: YOUR_AGENT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Docker?"}'
# Expected response: 200 OK with the answer
```

## Environment Variables Set
- `PORT`: 8000
- `ENVIRONMENT`: production
- `AGENT_API_KEY`: [YOUR_SECURE_API_KEY]
- `OPENAI_API_KEY`: [YOUR_OPENAI_OR_OPENROUTER_API_KEY]
- `REDIS_URL`: redis://redis:6379/0 (or external Redis database URL)

## Screenshots
Please save your screenshots in a folder named `screenshots/` in the root directory:
- `screenshots/dashboard.png`: Railway dashboard showing the deployed service and database status.
- `screenshots/running.png`: Service running/logs showing successful startup and requests.
- `screenshots/test.png`: Terminal/Postman screenshot showing the test command results (200 OK and 401/429 blocks).
