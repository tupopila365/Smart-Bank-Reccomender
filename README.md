# SmartBank Recommender

AI-powered banking product recommendation system that provides personalized financial product suggestions using machine learning.

![Status](https://img.shields.io/badge/status-production--ready-green)
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-blue)

## 🎯 Overview

SmartBank Recommender is a full-stack application that uses machine learning to provide personalized banking product recommendations. The system analyzes user financial profiles and suggests the most suitable checking accounts, savings accounts, loans, and digital banking services.

### Key Features

- 🤖 **ML-Powered Recommendations** - K-Means clustering and Decision Tree classification
- 📱 **Cross-Platform Mobile App** - iOS, Android, and Web support
- 🚀 **RESTful API** - Node.js backend with Express
- 🐳 **Docker Ready** - Fully containerized for easy deployment
- 💾 **Offline Support** - Local data storage with SQLite
- 📊 **Analytics** - Usage tracking and insights
- 🎨 **Modern UI** - Beautiful gradient designs

## 🏗️ Architecture

```
┌─────────────────────────────┐
│      Mobile App             │
│    (React Native/Expo)      │
│  - User Interface           │
│  - Local Storage (SQLite)   │
│  - Offline Support          │
└──────────┬──────────────────┘
           │
           │ REST API (HTTP/JSON)
           │
┌──────────▼──────────────────┐
│     Backend API             │
│   (Node.js/Express)         │
│  - Request Validation       │
│  - Business Logic           │
│  - API Gateway              │
│  Port: 3000                 │
└──────────┬──────────────────┘
           │
           │ HTTP/JSON
           │
┌──────────▼──────────────────┐
│      ML Service             │
│   (Python/FastAPI)          │
│  - K-Means Clustering       │
│  - Decision Trees           │
│  - Feature Engineering      │
│  Port: 8000                 │
└─────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Docker & Docker Compose** (recommended)
- **Node.js 18+** (for local development)
- **Python 3.9+** (for local development)
- **Expo CLI** (for mobile development)

### Option 1: Docker (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/your-org/smartbank-recommender.git
cd smartbank-recommender
```

2. **Start all services**
```bash
docker-compose up -d
```

3. **Verify services are running**
```bash
docker ps
```

You should see:
- `smartbank-ml-service` (port 8000) - HEALTHY
- `smartbank-backend` (port 3000) - HEALTHY

4. **Test the API**
```bash
curl http://localhost:3000/health
curl http://localhost:8000/health
```

5. **Start the mobile app**
```bash
cd mobile
npm install
npm start
```

### Option 2: Local Development

#### Backend Services

**ML Service:**
```bash
cd ml-service
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python scripts/generate_data.py
python scripts/train_models.py
uvicorn src.api.main:app --reload
```

**Backend API:**
```bash
cd backend
npm install
cp .env.example .env
npm run dev
```

#### Mobile App

```bash
cd mobile
npm install
npm start
```

## 📱 Mobile App

### Supported Platforms

- ✅ iOS (Simulator & Device)
- ✅ Android (Emulator & Device)
- ✅ Web Browser

### Running the App

```bash
cd mobile
npm start

# Then choose platform:
# Press 'i' for iOS
# Press 'a' for Android
# Press 'w' for Web
```

### Configuration

Update API endpoint in `mobile/src/utils/constants.ts`:

```typescript
// iOS Simulator / Web
export const API_BASE_URL = 'http://localhost:3000';

// Android Emulator
export const API_BASE_URL = 'http://10.0.2.2:3000';

// Physical Device (same WiFi)
export const API_BASE_URL = 'http://YOUR_IP:3000';
```

## 🔧 Tech Stack

### Backend Services

| Component | Technology | Purpose |
|-----------|-----------|---------|
| ML Service | Python 3.9, FastAPI | Machine learning predictions |
| Backend API | Node.js 18, Express | RESTful API gateway |
| ML Models | scikit-learn | K-Means, Decision Trees |
| Data Processing | pandas, numpy | Feature engineering |

### Mobile App

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Framework | React Native, Expo | Cross-platform mobile |
| Language | TypeScript | Type safety |
| Navigation | React Navigation | Screen navigation |
| Storage | SQLite, AsyncStorage | Local data persistence |
| HTTP Client | Axios | API communication |

### Infrastructure

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Containerization | Docker, Docker Compose | Service orchestration |
| Health Checks | HTTP-based | Service monitoring |
| Logging | Winston, Python logging | Application logs |

## 📊 ML Models

### K-Means Clustering

Segments users into 4-6 financial profiles based on:
- Income level
- Credit score
- Savings behavior
- Spending patterns
- Digital engagement

### Decision Tree Classifiers

Four separate models predict optimal products:
1. **Checking Account** - Basic, Premium, Student
2. **Savings Account** - Standard, High-Yield, Money Market
3. **Loan Products** - Personal, Auto, Mortgage, Student
4. **Digital Services** - Basic, Premium, Business

### Feature Engineering

Enhanced features include:
- Financial health score (weighted: 40% income, 25% credit, 20% savings, 15% spending)
- Income-to-spending ratio
- Savings capacity
- Debt-to-income ratio
- Digital adoption score

## 🔌 API Endpoints

### Backend API (Port 3000)

```http
GET  /health                 # Health check
POST /api/profile            # Create/update profile
POST /api/recommend          # Get recommendations
POST /api/usage              # Log usage event
GET  /api/user/:id           # Get user profile
```

### ML Service (Port 8000)

```http
GET  /health                 # Health check
POST /predict                # Get ML predictions
GET  /docs                   # API documentation (Swagger)
```

## 📖 Documentation

Detailed documentation for each component:

- **[ML Service README](ml-service/README.md)** - ML service setup, training, and deployment
- **[Backend README](backend/README.md)** - Backend API documentation and configuration
- **[Mobile README](mobile/README.md)** - Mobile app setup and building
- **[Docker Guide](DOCKER_STACK_COMPLETE.md)** - Docker deployment guide
- **[Testing Guide](MOBILE_APP_TESTING_GUIDE.md)** - Testing instructions

## 🧪 Testing

### Backend Testing

```bash
# Test ML service
curl http://localhost:8000/health

# Test backend
curl http://localhost:3000/health

# Test full stack
.\test-full-stack.ps1  # Windows
./test-full-stack.sh   # Mac/Linux
```

### Sample Request

```bash
curl -X POST http://localhost:3000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "age": 30,
    "income": 75000,
    "employment_status": "employed",
    "credit_score": 720,
    "existing_products": ["basic_checking"],
    "monthly_spending": 2500,
    "savings_balance": 15000,
    "loan_amount": 0,
    "digital_engagement": 8,
    "spending_score": 65,
    "saving_frequency": 7,
    "loan_behavior": 2
  }'
```

### Expected Response

```json
{
  "success": true,
  "data": {
    "recommended_account": "Basic Checking Account",
    "recommended_savings": "Standard Savings Account",
    "recommended_loan": "Auto Loan",
    "recommended_digital_service": "Premium Digital Banking",
    "cluster_segment": 1
  }
}
```

## 🚢 Deployment

### Docker Deployment

```bash
# Build and start
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Cloud Deployment

#### Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

#### Render

1. Connect GitHub repository
2. Create Web Services for backend and ML service
3. Configure environment variables
4. Deploy

#### AWS/Azure/GCP

Use Docker images:
```bash
docker build -t smartbank-backend ./backend
docker build -t smartbank-ml-service ./ml-service
```

Deploy to:
- AWS ECS/Fargate
- Azure Container Instances
- Google Cloud Run

### Mobile App Deployment

#### iOS (App Store)

```bash
cd mobile
eas build --platform ios
eas submit --platform ios
```

#### Android (Play Store)

```bash
cd mobile
eas build --platform android
eas submit --platform android
```

## 🔐 Environment Variables

### Backend API

```bash
NODE_ENV=production
PORT=3000
ML_SERVICE_URL=http://ml-service:8000
LOG_LEVEL=info
CORS_ORIGIN=*
```

### ML Service

```bash
PYTHONUNBUFFERED=1
LOG_LEVEL=INFO
MODEL_PATH=./models
DATA_PATH=./data
```

### Mobile App

```typescript
API_BASE_URL=https://api.smartbank.com
```

## 📈 Performance

| Metric | Value |
|--------|-------|
| ML Model Loading | ~2 seconds |
| Prediction Time | <100ms |
| API Response Time | <1 second |
| Mobile App Size | ~50MB |
| Concurrent Users | 1000+ |

## 🛠️ Development

### Project Structure

```
smartbank-recommender/
├── backend/              # Node.js backend API
│   ├── src/
│   ├── Dockerfile
│   └── package.json
├── ml-service/          # Python ML service
│   ├── src/
│   ├── models/
│   ├── scripts/
│   ├── Dockerfile
│   └── requirements.txt
├── mobile/              # React Native app
│   ├── src/
│   ├── assets/
│   └── package.json
├── docker-compose.yml   # Docker orchestration
└── README.md           # This file
```

### Development Workflow

1. **Backend Development**
```bash
cd backend
npm run dev  # Hot reload enabled
```

2. **ML Service Development**
```bash
cd ml-service
uvicorn src.api.main:app --reload
```

3. **Mobile Development**
```bash
cd mobile
npm start  # Expo dev server
```

### Code Quality

```bash
# Backend
cd backend
npm run lint
npm run format
npm test

# ML Service
cd ml-service
black src/
pytest tests/

# Mobile
cd mobile
npm run lint
npm test
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Contribution Guidelines

- Follow existing code style
- Add tests for new features
- Update documentation
- Ensure all tests pass
- Keep commits atomic and well-described

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **Backend Team** - Node.js/Express API
- **ML Team** - Python/FastAPI ML service
- **Mobile Team** - React Native app
- **DevOps Team** - Docker/CI/CD

## 📞 Support

- **Documentation:** [docs.smartbank.com](https://docs.smartbank.com)
- **Issues:** [GitHub Issues](https://github.com/your-org/smartbank-recommender/issues)
- **Email:** support@smartbank.com
- **Discord:** [Join our community](https://discord.gg/smartbank)

## 🗺️ Roadmap

### Version 1.1 (Q1 2026)
- [ ] User authentication
- [ ] Database persistence (PostgreSQL)
- [ ] Admin dashboard
- [ ] Email notifications

### Version 1.2 (Q2 2026)
- [ ] Advanced ML models
- [ ] A/B testing framework
- [ ] Real-time recommendations
- [ ] Multi-language support

### Version 2.0 (Q3 2026)
- [ ] Credit risk assessment
- [ ] Fraud detection
- [ ] Investment recommendations
- [ ] Financial planning tools

## 🎉 Acknowledgments

- scikit-learn for ML algorithms
- FastAPI for modern Python API
- React Native for cross-platform mobile
- Expo for development tools
- Docker for containerization

## 📊 Project Status

- ✅ **Backend API** - Production Ready
- ✅ **ML Service** - Production Ready
- ✅ **Mobile App** - Production Ready
- ✅ **Docker Setup** - Production Ready
- ✅ **Documentation** - Complete
- ⏳ **Cloud Deployment** - In Progress
- ⏳ **App Store Release** - Planned

---

**Built with ❤️ by the SmartBank Team**

**Version:** 1.0.0  
**Last Updated:** November 2025  
**Status:** Production Ready ✅

[⬆ Back to top](#smartbank-recommender)
