const { body } = require('express-validator');

export const profileValidationRules = [
  body('income')
    .exists()
    .withMessage('Income is required')
    .isNumeric()
    .withMessage('Income must be a number')
    .isFloat({ min: 0 })
    .withMessage('Income must be non-negative'),

  body('spending_score')
    .exists()
    .withMessage('Spending score is required')
    .isNumeric()
    .withMessage('Spending score must be a number')
    .isFloat({ min: 0, max: 100 })
    .withMessage('Spending score must be between 0 and 100'),

  body('saving_frequency')
    .exists()
    .withMessage('Saving frequency is required')
    .isNumeric()
    .withMessage('Saving frequency must be a number')
    .isFloat({ min: 0, max: 10 })
    .withMessage('Saving frequency must be between 0 and 10'),

  body('loan_behavior')
    .exists()
    .withMessage('Loan behavior is required')
    .isNumeric()
    .withMessage('Loan behavior must be a number')
    .isFloat({ min: 0, max: 5 })
    .withMessage('Loan behavior must be between 0 and 5'),
];

export const usageValidationRules = [
  body('user_id')
    .exists()
    .withMessage('User ID is required')
    .isInt({ min: 1 })
    .withMessage('User ID must be a positive integer'),

  body('action')
    .exists()
    .withMessage('Action is required')
    .isString()
    .withMessage('Action must be a string')
    .notEmpty()
    .withMessage('Action cannot be empty'),

  body('metadata')
    .optional()
    .isObject()
    .withMessage('Metadata must be an object'),
];
