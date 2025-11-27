# Backend Service Quick Start

## Installation

```bash
cd backend
npm install
```

## Development

```bash
npm run dev
```

Server will start on http://localhost:3000 with hot reload.

## Production Build

```bash
npm run build
npm start
```

## Environment Variables

Copy `.env.example` to `.env` and configure:

```env
PORT=3000
ML_SERVICE_URL=http://localhost:8000
NODE_ENV=development
LOG_LEVEL=info
CORS_ORIGIN=*
```

## Available Endpoints

- `GET /health` - Health check endpoint

## Testing

```bash
# Start the server
npm start

# In another terminal, run verification
node verify-setup.js
```

## Project Structure

- `src/app.ts` - Express application setup
- `src/server.ts` - Server entry point
- `src/middleware/` - Express middleware
- `src/routes/` - API route definitions
- `src/types/` - TypeScript type definitions
- `src/utils/` - Utility functions
- `src/controllers/` - Request handlers (to be added)
- `src/services/` - Business logic (to be added)

## Next Steps

Task 5 will add:
- Profile management endpoints
- Usage logging endpoints
- Recommendation endpoints
- ML service integration
