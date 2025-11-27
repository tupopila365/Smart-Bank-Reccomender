import { Request, Response, NextFunction } from 'express';
import logger from '../utils/logger';
import { HTTP_STATUS } from '../utils/constants';
import { UsageLog } from '../types';

// In-memory storage for usage logs (for demo purposes)
const usageLogs: Array<UsageLog & { id: number; timestamp: string }> = [];
let nextLogId = 1;

export const logUsage = async (
  req: Request,
  res: Response,
  next: NextFunction
): Promise<void> => {
  try {
    const usageLog: UsageLog = {
      user_id: req.body.user_id,
      action: req.body.action,
      metadata: req.body.metadata || {},
    };

    const logEntry = {
      id: nextLogId++,
      ...usageLog,
      timestamp: new Date().toISOString(),
    };

    usageLogs.push(logEntry);

    logger.info('Usage event logged', logEntry);

    res.status(HTTP_STATUS.CREATED).json({
      success: true,
      message: 'Usage event logged successfully',
      data: logEntry,
    });
  } catch (error) {
    next(error);
  }
};

export const getUsageLogs = async (
  req: Request,
  res: Response,
  next: NextFunction
): Promise<void> => {
  try {
    const userId = req.query.user_id ? parseInt(req.query.user_id as string, 10) : null;

    let logs = usageLogs;
    if (userId) {
      logs = usageLogs.filter((log) => log.user_id === userId);
    }

    res.status(HTTP_STATUS.OK).json({
      success: true,
      data: logs,
    });
  } catch (error) {
    next(error);
  }
};
