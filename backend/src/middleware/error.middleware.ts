import { Request, Response, NextFunction } from 'express';
import logger from '../utils/logger';
import { HTTP_STATUS, ERROR_MESSAGES } from '../utils/constants';

export interface AppError extends Error {
  statusCode?: number;
  isOperational?: boolean;
}

export const errorHandler = (
  err: AppError,
  req: Request,
  res: Response,
  next: NextFunction
): void => {
  const statusCode = err.statusCode || HTTP_STATUS.INTERNAL_SERVER_ERROR;
  const message = err.message || ERROR_MESSAGES.INTERNAL_ERROR;

  // Log error details
  logger.error('Error occurred', {
    method: req.method,
    path: req.path,
    statusCode,
    message,
    stack: err.stack,
    timestamp: new Date().toISOString(),
  });

  // Send error response
  res.status(statusCode).json({
    success: false,
    message,
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack }),
  });
};

export const notFoundHandler = (
  req: Request,
  res: Response,
  next: NextFunction
): void => {
  const error: AppError = new Error(`Route not found: ${req.originalUrl}`);
  error.statusCode = HTTP_STATUS.NOT_FOUND;
  next(error);
};
