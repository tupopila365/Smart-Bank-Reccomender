# How to Start SmartBank Recommender

## Quick Start (Docker - Recommended)

### 1. Start Backend Services

```bash
docker-compose up -d
```

This starts:
- ✅ ML Service on port 8000
- ✅ Backend API on port 3000

### 2. Verify Services

```bash
# Check containers are running
docker ps

# Test ML Service
curl http://localhost:8000/health

# Test Backend
curl http://localhost:3000/health
```

### 3. Start Mobile App

```bash
cd mobile
npm install  # First time only
npm start
```

Then:
- Press `i` for iOS Simulator
- Press `a` for Android Emulator
- Press `w` for Web Browser

## That's It! 🎉

Your entire project is now running:
- 🤖 ML Service: http://localhost:8000
- 🔌 Backend API: http://localhost:3000
- 📱 Mobile App: Running in Expo

---

## Alternative: Manual Start (Without Docker)

If you prefer not to use Docker:

### Terminal 1: ML Service
```bash
cd ml-service
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
python scripts/generate_data.py
python scripts/train_models.py
uvicorn src.api.main:app --reload
```

### Terminal 2: Backend API
```bash
cd backend
npm install  # First time only
npm run dev
```

### Terminal 3: Mobile App
```bash
cd mobile
npm install  # First time only
npm start
```

---

## Stopping the Project

### Docker
```bash
docker-compose down
```

### Manual
Press `Ctrl+C` in each terminal window

---

## Troubleshooting

### Docker containers won't start
```bash
# Check what's using the ports
netstat -ano | findstr :3000
netstat -ano | findstr :8000

# Stop any conflicting processes
Stop-Process -Id <PID> -Force

# Restart Docker
docker-compose down
docker-compose up -d
```

### Mobile app can't connect
1. Check backend is running: `curl http://localhost:3000/health`
2. For Android Emulator, update `mobile/src/utils/constants.ts`:
   ```typescript
   export const API_BASE_URL = 'http://10.0.2.2:3000';
   ```

### Port already in use
```bash
# Find and kill process using port 3000
netstat -ano | findstr :3000
Stop-Process -Id <PID> -Force
```

---

## First Time Setup

### Prerequisites
- Docker Desktop (for Docker method)
- Node.js 18+ (for manual method)
- Python 3.9+ (for manual method)
- Expo CLI (for mobile app)

### Install Prerequisites
```bash
# Install Expo CLI
npm install -g expo-cli

# Or use npx (no installation needed)
npx expo start
```

---

## Quick Commands Reference

```bash
# Start everything (Docker)
docker-compose up -d

# Stop everything (Docker)
docker-compose down

# View logs
docker-compose logs -f

# Restart a service
docker-compose restart backend
docker-compose restart ml-service

# Rebuild after code changes
docker-compose up -d --build

# Start mobile app
cd mobile && npm start
```

---

## What Runs Where

| Service | Port | URL |
|---------|------|-----|
| ML Service | 8000 | http://localhost:8000 |
| Backend API | 3000 | http://localhost:3000 |
| Mobile App | 8081 | http://localhost:8081 (Expo) |

---

## Testing the Setup

```bash
# Test ML Service
curl http://localhost:8000/health

# Test Backend
curl http://localhost:3000/health

# Test full stack
.\test-full-stack.ps1
```

---

**Need help?** Check `TROUBLESHOOTING.md` or `README.md`
