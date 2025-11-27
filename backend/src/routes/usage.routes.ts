import { Router } from 'express';
import { logUsage, getUsageLogs } from '../controllers/usage.controller';
import { usageValidationRules } from '../validators/profile.validator';
import { validate } from '../middleware/validation.middleware';

const router = Router();

// POST /api/usage - Log a usage event
router.post('/', validate(usageValidationRules), logUsage);

// GET /api/usage - Get usage logs (optional, for debugging)
router.get('/', getUsageLogs);

export default router;
