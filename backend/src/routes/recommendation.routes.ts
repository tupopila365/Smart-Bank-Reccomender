import { Router } from 'express';
import { getRecommendation } from '../controllers/recommendation.controller';
import { profileValidationRules } from '../validators/profile.validator';
import { validate } from '../middleware/validation.middleware';

const router = Router();

// POST /api/recommend - Get personalized recommendations
router.post('/', validate(profileValidationRules), getRecommendation);

export default router;
