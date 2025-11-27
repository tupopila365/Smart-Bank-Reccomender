import { Request, Response, NextFunction } from 'express';
import mlService from '../services/ml.service';
import logger from '../utils/logger';
import { HTTP_STATUS, ERROR_MESSAGES } from '../utils/constants';
import { UserProfile } from '../types';

export const getRecommendation = async (
  req: Request,
  res: Response,
  next: NextFunction
): Promise<void> => {
  try {
    const profile: UserProfile = {
      income: req.body.income,
      spending_score: req.body.spending_score,
      saving_frequency: req.body.saving_frequency,
      loan_behavior: req.body.loan_behavior,
    };

    logger.info('Requesting recommendation from ML Service', { profile });

    // Forward request to ML Service
    const recommendation = await mlService.predict(profile);

    logger.info('Recommendation received successfully', { recommendation });

    res.status(HTTP_STATUS.OK).json({
      success: true,
      data: recommendation,
    });
  } catch (error) {
    logger.error('Error getting recommendation', { error });

    // Handle ML service errors
    if (error instanceof Error) {
      res.status(HTTP_STATUS.BAD_GATEWAY).json({
        success: false,
        message: ERROR_MESSAGES.ML_SERVICE_ERROR,
        error: error.message,
      });
      return;
    }

    next(error);
  }
};
