import { Router, Request, Response } from 'express';

const router = Router();

router.get('/health', (req: Request, res: Response) => {
  res.status(200).json({
    success: true,
    message: 'Backend service is healthy',
    timestamp: new Date().toISOString(),
    service: 'smartbank-backend',
  });
});

export default router;
