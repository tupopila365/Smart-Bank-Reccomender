import { Request, Response, NextFunction } from 'express';
import logger from '../utils/logger';
import { HTTP_STATUS } from '../utils/constants';
import { UserProfile } from '../types';

// In-memory storage for profiles (for demo purposes)
// In production, this would be a database
const profiles = new Map<number, UserProfile & { id: number; created_at: string; updated_at: string }>();
let nextId = 1;

export const createProfile = async (
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

    const id = nextId++;
    const timestamp = new Date().toISOString();
    const storedProfile = {
      id,
      ...profile,
      created_at: timestamp,
      updated_at: timestamp,
    };

    profiles.set(id, storedProfile);

    logger.info('Profile created successfully', { id, profile });

    res.status(HTTP_STATUS.CREATED).json({
      success: true,
      message: 'Profile created successfully',
      data: storedProfile,
    });
  } catch (error) {
    next(error);
  }
};

export const getProfile = async (
  req: Request,
  res: Response,
  next: NextFunction
): Promise<void> => {
  try {
    const id = parseInt(req.params.id, 10);

    if (isNaN(id)) {
      res.status(HTTP_STATUS.BAD_REQUEST).json({
        success: false,
        message: 'Invalid user ID',
      });
      return;
    }

    const profile = profiles.get(id);

    if (!profile) {
      res.status(HTTP_STATUS.NOT_FOUND).json({
        success: false,
        message: 'User profile not found',
      });
      return;
    }

    logger.info('Profile retrieved successfully', { id });

    res.status(HTTP_STATUS.OK).json({
      success: true,
      data: profile,
    });
  } catch (error) {
    next(error);
  }
};
