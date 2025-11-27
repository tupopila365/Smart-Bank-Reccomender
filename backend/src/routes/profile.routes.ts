import { Router } from 'express';
import { createProfile, getProfile } from '../controllers/profile.controller';
import { profileValidationRules } from '../validators/profile.validator';
import { validate } from '../middleware/validation.middleware';

const router = Router();

// POST /api/profile - Create a new user profile
router.post('/', validate(profileValidationRules), createProfile);

// GET /api/user/:id - Get user profile by ID
router.get('/:id', getProfile);

export default router;
