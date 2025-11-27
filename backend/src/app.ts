import express, { Application } from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { loggingMiddleware } from './middleware/logging.middleware';
import { errorHandler, notFoundHandler } from './middleware/error.middleware';
import healthRoutes from './routes/health.routes';
import profileRoutes from './routes/profile.routes';
import usageRoutes from './routes/usage.routes';
import recommendationRoutes from './routes/recommendation.routes';
import logger from './utils/logger';

// Load environment variables
dotenv.config();

const app: Application = express();

// CORS configuration
const corsOptions = {
  origin: process.env.CORS_ORIGIN || '*',
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true,
};

// Middleware
app.use(cors(corsOptions));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(loggingMiddleware);

// Routes
app.use('/', healthRoutes);
app.use('/api/profile', profileRoutes);
app.use('/api/user', profileRoutes);
app.use('/api/usage', usageRoutes);
app.use('/api/recommend', recommendationRoutes);

// Error handling
app.use(notFoundHandler);
app.use(errorHandler);

logger.info('Application initialized successfully');

export default app;
